# -*-coding:utf-8 -*-
# Time:2021/1/25 11:15 上午
from django.contrib import admin
from django.urls import path,include,re_path
from . import views
urlpatterns = [
    #发送验证码
    re_path('^smsCode/(?P<mobile>1[3-9]\d{9})$', views.SmsCodeAPIView.as_view()),


]