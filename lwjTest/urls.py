"""lwjTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    #验证码
    path('sms/',include('apps.verification.urls')),
    # 用户
    re_path('^',include('apps.users.urls')),
    #api
    path('api/', include('apps.apiTest.urls')),
    #case
    path('case/', include('apps.case.urls')),
    #阐道
    path('chandao/', include('apps.chanDao.urls')),
    #报告
    path('report/',include('apps.report.urls')),
    #系统
    path('question/',include('apps.system.urls')),
    #任务
    path('task/',include('apps.task.urls')),
    #生成测试用例
    path('generate/',include('apps.generateCase.urls'))


]
