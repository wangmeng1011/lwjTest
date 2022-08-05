# -*-coding:utf-8 -*-
# Time:2021/1/26 4:41 下午
import re
from django.contrib.auth.backends import ModelBackend
from .models import Users
from utils.aesPassword import aes_decode
def jwt_response_payload_handler(token, user=None, request=None):
    """
    重写JWT登录视图的构造响应数据函数,多追加 user_id和username
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        "status":0,
        "msg":"ok",
        "results":{
            'token': token,
            'user_id': user.id,
            'username': user.username,
            'email':user.email,
            'name':user.name,
            # 'is_staff':user.is_staff
            }
        }

def get_user_by_account(account):
    """
    :param account: 可能是手机号，也可以能用户名
    :return:
    """
    try:
        #先判断是否是手机号
        if re.match("1[3-9]\d{9}",account):
            user = Users.objects.get(mobile=account)
        #用户名
        else:
            user = Users.objects.get(username=account)
    except:
        return None
    else:
        return user

class UsernameMobileAuthBackend(ModelBackend):
    """
    修改Django的认证类,为了实现多账号登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        # #站点登录密码不加密
        # if  request.path=="/admin/login":
        #     if user and user.check_password(password):
        #         return user
        #     else:
        #         return None
        # else:
            #密码解密
        try:
            if request.path == "/admin/login/":
                if user and user.check_password(password):
                    return user
                else:
                    return None
        except:
            password = aes_decode(password, username)
            # 判断密码是否正确
            if user and user.check_password(password):
                return user
            else:
                return None

