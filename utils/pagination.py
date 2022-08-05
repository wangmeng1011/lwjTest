# -*-coding:utf-8 -*-
# Time:2021/2/6 8:31 下午
from rest_framework.pagination import PageNumberPagination

class MyPageNumberPagination(PageNumberPagination):
    """
    自定义分页类
    """
    #每页显示多少条
    page_size = 20
    #url中每页显示条数的参数
    page_size_query_param = "size"
    #url中页码的参数
    page_query_param = "page"

