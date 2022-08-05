# -*-coding:utf-8 -*-

# Time:2021/2/24 5:59 下午
from rest_framework import serializers
from .models import FormalBug,SyetemQuestion
class FormalBugSerializer(serializers.ModelSerializer):
    """
    现网问题统计
    """
    class Meta:
        model = FormalBug
        fields = "__all__"

class SyetemQuestionSerializer(serializers.ModelSerializer):
    """
    现网问题统计
    """
    class Meta:
        model = SyetemQuestion
        fields = "__all__"