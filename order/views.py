import time

from django.db import transaction
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cart.models import Cart
from users.models import Addr
from .models import Order, OrderGoods, Comment
from .serializers import OrderSerializer, OrderGoodsSerializer, CommentSerializer
from .permissions import OrderPermission
from rest_framework import status, mixins


class OrderView(GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # 指定商品过滤的字段
    filterset_fields = ['status']
    # 设置认证用户才能有权限访问
    permission_classes = [IsAuthenticated, OrderPermission]

    def create(self, request, *args, **kwargs):
        """提交订单视图"""
        # 获取请求参数
        addr = request.data.get('addr')
        # 判断收货地址是存在
        if not Addr.objects.filter(id=addr, user=request.user).exists():
            return Response({'error': "订单创建失败，传入的收货地址ID有误！"},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 将收货地址拼接为字符串
        aobj = Addr.objects.get(id=addr)
        addr_str = '{}{}{}{}  {}   {}'.format(aobj.province, aobj.city,
                                              aobj.county, aobj.address,
                                              aobj.name, aobj.phone)
        # 获取购物车中选中的商品
        cart_goods = Cart.objects.filter(user=request.user, is_checked=True)
        if not cart_goods.exists():
            return Response({'error': "订单创建失败，未选中商品"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 生成一个订单编号:时间戳(精确到秒) +用户id
        order_code = str(int(time.time())) + str(request.user.id)

        # 设置一个事务保存的节点
        save_id = transaction.savepoint()

        try:
            # 创建订单
            order = Order.objects.create(user=request.user, addr=addr_str,
                                         order_code=order_code, amount=0)

            # 保存商品总价
            amount = 0
            # 遍历购物车中选中所有的商品
            for cart in cart_goods:
                # 获取购买商品的数量
                num = cart.number
                # 获取商品的价格
                price = cart.goods.price
                # 将价格进行累加
                amount += price * num
                # 判断商品购买数量是否大于商品库存
                if cart.goods.stock > num:
                    # 修改商品的库存和销量并且保存
                    cart.goods.stock -= num
                    cart.goods.sales += num
                    cart.goods.save()
                else:
                    # 事务回滚
                    transaction.savepoint_rollback(save_id)
                    return Response({'error': "创建失败，商品`{}`库存不足".format(cart.goods.title)},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                # 在订单商品表中新增一条数据
                OrderGoods.objects.create(order=order, goods=cart.goods,
                                          price=price, number=num)

                # 删除购物车中该商品记录
                cart.delete()
            # 修改订单的金额
            order.amount = amount
            order.save()
        except Exception as e:
            # 事务回滚
            transaction.savepoint_rollback(save_id)
            return Response({'error': "服务处理异常，订单创建失败！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # 提交事务保存数据到数据库
            transaction.savepoint_commit(save_id)
            # 返回结果
            ser = self.get_serializer(order)
            return Response(ser.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """获取订单列表"""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取订单的详情"""
        # 获取订单对象
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 获取订单中的商品信息
        goods = OrderGoods.objects.filter(order=instance)
        # 对订单中的商品信息进行序列化
        order_goods = OrderGoodsSerializer(goods, many=True)
        # 将订单中的商品信息一起返回
        result = serializer.data
        result['goods_list'] = order_goods.data

        return Response(result)

    def close_order(self, request, *args, **kwargs):
        """关闭订单"""
        # 获取到订单对象
        obj = self.get_object()
        # 校验订单是否处于未支付的状态
        if obj.status != 1:
            return Response({'error': "只能取消未支付的订单"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 将订单状态改为关闭
        obj.status = 6
        # 保存
        obj.save()
        # 返回结果
        return Response({'message': "取消成功，已关闭订单"})


class CommentView(GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin
                  ):
    """商品评价的接口"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    # 配置查询评价信息的过滤参数
    filterset_fields = ['goods', 'order']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """商品评价的接口"""
        # 获取参数
        order = request.data.get('order')
        # 校验订单编号是否为空
        if not order:
            return Response({'error': "订单id不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 订单是否存在，并且订单处于`待评价`的状态
        if not Order.objects.filter(id=order).exists():
            return Response({'error': "订单ID有误！"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        order_obj = Order.objects.get(id=order)
        if order_obj.user != request.user:
            return Response({'error': "没有评论该订单的权限！"}, status=status.HTTP_403_FORBIDDEN)
        if order_obj.status != 4:
            return Response({'error': "订单不处于待评论状态！"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 获取订单评论详情参数
        comment = request.data.get('comment')
        if not isinstance(comment, list):
            return Response({'error': "订单评论参数comment格式有误！"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 设置一个事务保存的节点
        save_id = transaction.savepoint()
        try:
            for item in comment:
                # 遍历参数中的商品评论信息
                # 校验参数是否有误！
                if not isinstance(item, dict):
                    return Response({'error': "订单评论参数comment格式有误！"},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                # 获取当前这条评论信息的商品id
                goods = item.get('goods', None)
                if not OrderGoods.objects.filter(order=order_obj, goods__id=goods).exists():
                    return Response({'error': "订单中没有id为{}的商品！".format(goods)},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                # 往item中添加订单id和用户id
                item['user'] = request.user.id
                item['goods'] = goods

                # 添加一条评论记录
                ser = CommentSerializer(data=item)
                ser.is_valid()
                ser.save()

            # 修改订单的状态为已完成
            order.status = 5
            order.save()
        except Exception as e:
            # 事务回滚
            transaction.savepoint_rollback(save_id)
            return Response({'error': "评论失败"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        else:
            # 提交事务
            transaction.savepoint_commit(save_id)
            return Response({'message': "评论成功"}, status=status.HTTP_201_CREATED)
