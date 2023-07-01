from django.contrib import admin
from .models import Order, OrderGoods, Comment


# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'order_code', 'pay_type', 'addr']


@admin.register(OrderGoods)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order', 'goods', 'price', 'number']


@admin.register(Comment)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'goods', 'content', 'rate', 'star']
