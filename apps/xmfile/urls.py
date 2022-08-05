# -*-coding:utf-8 -*-
# Time:2022/7/6 10:14 上午
from django.urls import path,include,re_path
from . import views
from rest_framework.routers import DefaultRouter
rouer = DefaultRouter()
#
rouer.register('xmind',views.XmFileViewSet)

urlpatterns = [
    #上传xmind文件
    path('file', views.UploadFile.as_view()),
    path('file/<pk>', views.DownFile.as_view()),
]+rouer.urls