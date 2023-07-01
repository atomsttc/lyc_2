"""
购物车模块序列化器
"""
from goods.Serializer import GoodsSerializer
from .models import Cart
from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    """写入：购物车序列化器"""
    class Meta:
        model = Cart
        fields = "__all__"


class ReadCartSerializer(serializers.ModelSerializer):
    """读取：购物车信息序列化器"""
    goods = GoodsSerializer()

    class Meta:
        model = Cart
        fields = "__all__"
