# -*-coding:utf-8 -*-
# Time:2021/4/23 9:56 上午
from rest_framework.serializers import ModelSerializer
from .models import GenerateCase,GenerateCaseRunRecord,GenerateRunStepRecord,GenerateCaseName
from rest_framework.serializers import ValidationError
class GenerateCaseSerializer(ModelSerializer):
    """
    导入测试用例
    """
    class Meta:
        model = GenerateCase
        fields = "__all__"

class GenerateCaseRunRecordSerializer(ModelSerializer):
    """
    用例运行记录
    """
    class Meta:
        model = GenerateCaseRunRecord
        fields = "__all__"

class GenerateRunStepRecordSerializer(ModelSerializer):
    """
    用例步骤记录
    """
    class Meta:
        model = GenerateRunStepRecord
        fields = "__all__"

class GenerateCaseNameSerializer(ModelSerializer):
    """
    用例
    """
    step = GenerateCaseSerializer(many=True)
    class Meta:
        model = GenerateCaseName
        fields = ['id','name','step']
