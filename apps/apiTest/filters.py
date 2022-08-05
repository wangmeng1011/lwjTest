# -*-coding:utf-8 -*-
# Time:2022/8/3 2:27 下午
import django_filters
from .models import Api
class ApiFilter(django_filters.FilterSet):
    class Meta:
        models = Api
        fields = {
            'name':['icontains'],
        }