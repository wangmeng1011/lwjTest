# -*-coding:utf-8 -*-
# __author__ = 'wuhongbin'
# Time:2021/1/25 7:21 下午
from rest_framework.response import Response

class ApiResponse(Response):
    def __init__(self,status=0,msg="ok",results=None,http_status=None,headers=None,exception=None,**kwargs):
        data={
            "status":status,
            "msg":msg,
        }
        if results is not None:
            data['result']=results
        #字典更新
        data.update(kwargs)
        super().__init__(data=data,status=http_status,headers=headers,exception=exception)