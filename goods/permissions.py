from rest_framework import permissions


class CollectPermission(permissions.BasePermission):
    """收藏对象操作权限"""

    def has_object_permission(self, request, view, obj):

        # 如果不是管理员，则判断操作的用户对象和登录的用户对象是否未同一个用户
        return obj.user == request.user
