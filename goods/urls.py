
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('index/', views.IndexView.as_view()),
    # 商品列表接口
    path('goods/', views.GoodsView.as_view({
        'get': 'list'
    })),
    # 获取单个商品接口
    path('goods/<int:pk>/', views.GoodsView.as_view({
        'get': 'retrieve'
    })),
    # 收藏商品和获取收藏列表
    path('collect/', views.CollectView.as_view({
        'post': 'create',
        "get": "list"
    })),
    # 取消收藏
    path('collect/<int:pk>/', views.CollectView.as_view({
        'delete': 'destroy'
    })),
    # 获取商品分类
    path('group/', views.GoodsGroupView.as_view({
        "get": "list"
    }))
]
