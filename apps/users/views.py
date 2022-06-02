from django.shortcuts import render
from django.contrib.auth.models import AbstractUser
from .serializers import UserSerializer
from rest_framework.views import APIView
from .models import Users
from utils.apiResponse import ApiResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView,ListCreateAPIView
from celery_tasks.email.tasks import send_verify_email
from utils.aesPassword import aes_decode
from ..users.permission import MyPermission
from ..users.authorizations import JWTAuthentication
from utils.pagination import MyPageNumberPagination
class UsernameView(APIView):
    """
    用户名是否已注册
    """
    def get(self, request, username):
        """
        :param request:
        :param username: 用户名
        :return:
        """
        # if username_type=="1":
        username_count = Users.objects.filter(username=username).count()
        #0表示数据库不存在该username
        if username_count==0:
            return ApiResponse()
        else:
            return ApiResponse(results="username:{}已注册".format(username),http_status=status.HTTP_400_BAD_REQUEST,status=1)
        # elif username_type=="2":
        #     username_count = Users.objects.filter(username=username).count()
        #     #0表示数据库存在该username
        #     if username_count==0:
        #         return ApiResponse()
        #     else:
        #         return ApiResponse(results="username:{}未注册".format(username), http_status=status.HTTP_400_BAD_REQUEST,
        #                            status=1)
        # else:
        #     return ApiResponse(results="type类型不存在", http_status=status.HTTP_400_BAD_REQUEST,
        #                        status=1)


class MobileView(APIView):
    """
    手机号是否已注册
    """
    def get(self, request, mobile, mobile_type):
        """
        :param request:
        :param mobile: 手机号
        :param mobile_type: 1：注册 2：修改密码
        :return:
        """
        if mobile_type=="1":
            username_count = Users.objects.filter(mobile=mobile).count()
            #0表示数据库不存在该mobile
            if username_count==0:
                return ApiResponse()
            else:
                return ApiResponse(msg="mobile:{}已注册".format(mobile),http_status=status.HTTP_400_BAD_REQUEST,status=1)
        elif mobile_type=="2":
            username_count = Users.objects.filter(mobile=mobile).count()
            #1表示数据库存在该mobile
            if username_count==1:
                #返回用户id和mobile，提供修改密码的主键
                user = Users.objects.filter(mobile=mobile)[0]
                user_data = {
                    "user_id":user.id,
                    "mobile":user.mobile
                }
                return ApiResponse(results=user_data)
            else:
                return ApiResponse(msg="mobile:{}未注册".format(mobile), http_status=status.HTTP_400_BAD_REQUEST,
                                   status=1)
        else:
            return ApiResponse(msg="type类型不存在", http_status=status.HTTP_400_BAD_REQUEST,
                               status=1)

class UserView(UpdateAPIView,ListCreateAPIView):
    """
    UpdateAPIView：修改密码
    ListCreateAPIView:注册用户/用户列表
    """
    serializer_class = UserSerializer
    pagination_class = MyPageNumberPagination
    #重写查询集
    def get_queryset(self):
        if len(self.request.query_params)==0:
            #没有通过条件查询返回所有用户
            return Users.objects.all()
        else:
            #通过username模糊查询
            return Users.objects.filter(username__contains=self.request.query_params.get("username","")).filter(mobile__contains=self.request.query_params.get("mobile","")).filter(name__contains=self.request.query_params.get("name",""))

class UserAdmin(APIView):
    """
    升级权限
    """
    # permission_classes = [MyPermission]
    # authentication_classes = [JWTAuthentication]
    def post(self, request, mobile):
        mobile_count = Users.objects.filter(mobile=mobile).count()
        if mobile_count==0:
            #数据库不存在该账户
            return ApiResponse(msg="mobile:{}未注册".format(mobile), http_status=status.HTTP_400_BAD_REQUEST,status=1)
        else:
            user = Users.objects.filter(mobile=mobile)[0]
            if user.is_staff==True:
                return ApiResponse(msg="mobile:{}已经是管理员".format(mobile), http_status=status.HTTP_400_BAD_REQUEST,status=1)
            else:
                user.is_staff=True
                user.is_superuser=True
                user.save()
                return ApiResponse(msg="权限升级成功")



