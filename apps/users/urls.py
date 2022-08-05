# -*-coding:utf-8 -*-
# Time:2021/1/25 11:14 上午
from django.conf.urls import url
from django.urls import path,include,re_path
from . import views
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    #username验证
    re_path(r'^username/(?P<username>\w{5,20})',views.UsernameView.as_view()),
    #mobile验证
    re_path(r'^mobile/(?P<mobile>1[3-9]\d{9})/(?P<mobile_type>[1-2])', views.MobileView.as_view()),
    #注册账号
    re_path('^register$', views.UserView.as_view()),
    #修改密码
    path('password/<pk>', views.UserView.as_view()),
    #升级为管理员
    path('jurisdiction/<mobile>', views.UserAdmin.as_view()),


    #jwt自带的登录(登录后自动生成token)
    re_path('^login$',obtain_jwt_token),

]