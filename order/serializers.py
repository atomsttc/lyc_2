from rest_framework import serializers

from goods.Serializer import GoodsSerializer
from order.models import Order, OrderGoods, Comment


class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单商品序列化器"""
    goods = GoodsSerializer()

    class Meta:
        model = OrderGoods
        fields = ['goods', 'number', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    ordergoods_set = OrderGoodsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """商品评价序列化器"""

    class Meta:
        model = Comment
        fields = "__all__"
