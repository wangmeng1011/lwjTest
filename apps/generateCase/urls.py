# -*-coding:utf-8 -*-
# Time:2021/2/20 2:02 下午
from django.urls import path,include,re_path
from . import views
from rest_framework.routers import DefaultRouter

rouer = DefaultRouter()
#用例步骤
rouer.register('step',views.GenerateCaseRunRecordViewSet,basename='step')


urlpatterns = [
            #导入测试用例
            path('case', views.GenerateCaseAPIView.as_view()),
            #执行测试用例
            path('run',views.CaseRunApiView.as_view()),
            path('run/<pk>',views.CaseRunApiView.as_view()),
            #清洗headers
            path('clean',views.CaseHeadersClean.as_view()),
            #汇总用例
            path('summary',views.SummaryCaseApiView.as_view())
              ]+rouer.urls

