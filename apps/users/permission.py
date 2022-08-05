# -*-coding:utf-8 -*-
# Time:2021/2/20 10:17 上午
from rest_framework.permissions import BasePermission
class MyPermission(BasePermission):
    """
    权限
    """
    message = {"status":"3","msg":"没有管理员权限，请联系管理员"}
    def has_permission(self, request, view):
        # 内置封装的方法
        '''
        判断该用户有没有权限
        '''
        if request.method in ["POST","PUT","DELETE"]:
            if request.user.is_staff == True:   # 是VIP用户
                return True
            else:
                return False
        else:
            return True