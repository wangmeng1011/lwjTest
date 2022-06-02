from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *


@admin.register(GenerateCaseName)
class ProjectAdmin(admin.ModelAdmin):
    """导入用例名称"""
    list_display = ['name','is_delete']

@admin.register(GenerateCase)
class ProjectAdmin(admin.ModelAdmin):
    """解析测试用例"""
    list_display = ['host','path','method','request_type']

@admin.register(GenerateCaseRunRecord)
class ProjectAdmin(admin.ModelAdmin):
    """导入的用例运行记录"""
    list_display = ['name','create_time']

@admin.register(GenerateRunStepRecord)
class ProjectAdmin(admin.ModelAdmin):
    """导入的用例运行步骤记录"""
    list_display = ['url','http_method','data']
