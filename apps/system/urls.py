# -*-coding:utf-8 -*-
# __author__ = 'wuhongbin'
# Time:2021/2/20 4:05 下午
from django.urls import path,include,re_path
from . import views
from rest_framework.routers import DefaultRouter

rouer = DefaultRouter()
#现网问题
rouer.register('bug',views.FormalbugViewsets,basename='Formalbug')
#系统问题
rouer.register('',views.SystemQuestionViewsets,basename='SystemQuestion')
urlpatterns = [

              ]+rouer.urls