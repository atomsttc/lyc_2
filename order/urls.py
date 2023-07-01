from django.urls import path
from . import views

# 订单模块的api路由配置
urlpatterns = [
    # 提交订单的接口
    path('submit/', views.OrderView.as_view({
        "post": "create"
    })),
    # 获取订单列表的接口
    path('order/', views.OrderView.as_view({
        "get": "list"
    })),
    # 获取单个订单的详情数据
    path('order/<int:pk>/', views.OrderView.as_view({
        "get": "retrieve",
        # 取消订单
        "put": "close_order"
    })),
    # # 商品评价的接口
    path('comment/', views.CommentView.as_view({
        "post": "create",
        "get": "list",
    })),
    # # 订单支付页面地址获取
    # path('alipay/', views.OrderPayView.as_view({
    #     # 生成支付页面地址
    #     'post': "create",
    #     # 查询支付结果
    #     "get": "get_pay_result"
    # })),
    #
    # path('alipay/callback/', views.OrderPayView.as_view({
    #     # 支付宝回调的接口地址
    #     'post': "alipay_callback_result",
    # })),
]
