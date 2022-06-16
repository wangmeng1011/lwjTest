from django.shortcuts import render
import os
import re
import json
from datetime import datetime
from .run_api import run_request
from urllib import parse
from utils.dingDing import DingDing
from .models import GenerateCase,GenerateCaseName,GenerateCaseRunRecord
from .serializers import GenerateCaseNameSerializer,GenerateCaseSerializer
from rest_framework.views import APIView
from utils.apiResponse import ApiResponse
from lwjTest.settings import logger
from .analysis_file import analysis_file
from .run_case import run_case_list
from lwjTest.settings import UPLOAD_ROOT
from utils.pagination import MyPageNumberPagination
from rest_framework.viewsets import ModelViewSet
from utils.primordial_sql import my_custom_sql
class GenerateCaseAPIView(APIView):
    """
    解析文件
    """
    def post(self, request):
        #获取上传文件
        file = request.FILES.get('file',None)
        case_name = request.data.get("case_name","")
        if file is None:
            return ApiResponse(status=1,msg="请选择上传文件")
        else:
            if file.name.endswith(('.har')):
                destinstion = open(os.path.join(UPLOAD_ROOT,file.name),'wb+')
            else:
                return ApiResponse(status=1,msg="文件格式错误，只支持.har文件")
            try:
                for chunk in file.chunks():
                    destinstion.write(chunk)
                destinstion.close()
            except Exception as e:
                return ApiResponse(status=1,msg="数据异常")
        #解析文件
        analysis_file(file,case_name)

        # 查询用例ID
        case_obj = GenerateCaseName.objects.filter(name=case_name, is_delete=0)

        name_id = case_obj[0].id

        return ApiResponse(msg="解析成功", **{'name_id': name_id})

class CaseRunApiView(APIView):
    """
    用例
    """

    def get(self,request):
        case = GenerateCaseName.objects.filter(is_delete=0)
        pg = MyPageNumberPagination()
        page_case = pg.paginate_queryset(queryset=case, request=request, view=self)
        serializer = GenerateCaseNameSerializer(instance=page_case,many=True).data
        return pg.get_paginated_response(serializer)

    def post(self,request,*args, **kwargs):
        case_id_list = request.data.get("case_id_list")
        result_dict = run_case_list(case_id_list)
        return ApiResponse(results={"url":result_dict})

    def put(self,request,pk=None):
        name = request.data.get['name',None]
        case_name = GenerateCaseName.objects.get(pk=pk)
        case_name.name = name
        case_name.save()
        return ApiResponse(msg="更新成功")

    def delete(self,request,pk=None):
        case = GenerateCaseName.objects.get(pk=pk)
        case.is_delete = True
        case.save()
        logger.info("删除用例id:{}".format(pk))
        return ApiResponse(msg="删除成功")

class GenerateCaseRunRecordViewSet(ModelViewSet):
    """
    用例步骤
    """
    queryset = GenerateCase.objects.all()
    pagination_class = MyPageNumberPagination
    serializer_class = GenerateCaseSerializer

class CaseHeadersClean(APIView):
    def post(self,request,*args,**kwargs):
        name_id = request.data.get("name_id")
        try:
            #处理304的请求
            sql = "update fusion_generate_case set expect_code=200 where expect_code=304 and name_id={}".format(name_id)
            logger.info(sql)
            my_custom_sql(sql)

            sql = "select id,headers from fusion_generate_case where name_id={}".format(name_id)
            result = my_custom_sql(sql)
            for headers in result:
                special_str = "{'name': 'If-None-Match', 'value':"
                if special_str in headers[1]:
                    special_header = headers[1].split(special_str)
                    special_header_1 = special_header[1].split("},",1)
                    header = special_header[0]+"{'name': 'If-None-Match', 'value':''},"+special_header_1[1]
                    sql = 'update fusion_generate_case set headers="{}" where id={}'.format(header, headers[0])
                    my_custom_sql(sql)

            #分销
            sql = "select id,headers from fusion_generate_case where name_id={}".format(name_id)
            result = my_custom_sql(sql)
            for header in result:
                data=header[1]
                data_sid = re.findall( ".*sid=(.*?);",data)
                if len(data_sid)!=0:
                    data_sid = data.replace(data_sid[0],"{{sales_sid}}")
                else:
                    data_sid = data

                data_LX_WXSRF_JTOKEN=re.findall(".*LX-WXSRF-JTOKEN=(.*?)'",data_sid)
                if len(data_LX_WXSRF_JTOKEN)!=0:
                    data_LX_WXSRF_JTOKEN = data_sid.replace(data_LX_WXSRF_JTOKEN[0],"{{sales_LX_WXSRF_JTOKEN}}")
                else:
                    data_LX_WXSRF_JTOKEN=data_sid
                sql = 'update fusion_generate_case set headers="{}" where id={}'.format(data_LX_WXSRF_JTOKEN, header[0])
                logger.info(sql)
                my_custom_sql(sql)

                # 更新支付系统的cookies
                sql='select id,host,headers from fusion_generate_case where host="http://pay-staging.liweijia.com" and name_id={}'.format(name_id)
                result = my_custom_sql(sql)
                for i in result:
                    data=i[2]
                    #替换sid
                    data_sid=re.findall( ".*sid=(.*?);",data)
                    if len(data_sid)!=0:
                        data_sid = data.replace(data_sid[0],"{{pay_sid}}")
                    else:
                        data_sid = data

                    data_LX_WXSRF_JTOKEN=re.findall(".*LX-WXSRF-JTOKEN=(.*?);",data_sid)
                    if len(data_LX_WXSRF_JTOKEN)!=0:
                        data_LX_WXSRF_JTOKEN = data_sid.replace(data_LX_WXSRF_JTOKEN[0],"{{pay_LX_WXSRF_JTOKEN}}")
                    else:
                        data_LX_WXSRF_JTOKEN=data_sid

                    data_LX_WXSRF_JTOKEN_1=re.findall(".*LX-WXSRF-JTOKEN=(.*?)'",data_LX_WXSRF_JTOKEN)

                    if len(data_LX_WXSRF_JTOKEN_1)!=0 and len(data_LX_WXSRF_JTOKEN_1[0])<50:
                        data_LX_WXSRF_JTOKEN_1 = data_LX_WXSRF_JTOKEN.replace(data_LX_WXSRF_JTOKEN_1[0],"{{pay_LX_WXSRF_JTOKEN}}")
                    else:
                        data_LX_WXSRF_JTOKEN_1=data_LX_WXSRF_JTOKEN

                    data_pay_session=re.findall(".*pay_session=(.*?);",data_LX_WXSRF_JTOKEN_1)
                    if len(data_pay_session)!=0:
                        data_pay_session = data_LX_WXSRF_JTOKEN_1.replace(data_pay_session[0],"{{pay_pay_session}}")
                    else:
                        data_pay_session = data_LX_WXSRF_JTOKEN_1

                    data_pay_session_1=re.findall(".*pay_session=(.*?)'",data_pay_session)
                    if len(data_pay_session_1)!=0 and len(data_pay_session_1[0])<50:
                        data_pay_session_1 = data_pay_session.replace(data_pay_session_1[0],"{{pay_pay_session}}")
                    else:
                        data_pay_session_1 = data_pay_session

                    data_XSRF_TOKEN=re.findall(".*XSRF-TOKEN=(.*?)'",data_pay_session_1)
                    if len(data_XSRF_TOKEN)!=0:
                        data_XSRF_TOKEN = data_pay_session_1.replace(data_XSRF_TOKEN[0],"{{pay_XSRF_TOKEN}}")
                    else:
                        data_XSRF_TOKEN = data_pay_session_1

                    data_X_XSRF_TOKEN=re.findall(".*X-XSRF-TOKEN', 'value': '(.*?)'",str(data_XSRF_TOKEN))
                    if len(data_X_XSRF_TOKEN)!=0:
                        data_X_XSRF_TOKEN = data_pay_session.replace(data_X_XSRF_TOKEN[0],"{{pay_X_XSRF_TOKEN}}")
                    else:
                        data_X_XSRF_TOKEN = data_XSRF_TOKEN

                    sql = 'update fusion_generate_case set headers="{}" where id={}'.format(data_X_XSRF_TOKEN, i[0])
                    my_custom_sql(sql)
                #site系统
                sql = "select id,headers from fusion_generate_case where host='http://siteadmin-staging.liweijia.com' and name_id={}".format(name_id)
                result = my_custom_sql(sql)
                for header in result:
                    data = header[1]
                    data_sid = re.findall( ".*sid=(.*?);",data)
                    if len(data_sid)!=0:
                        data_sid = data.replace(data_sid[0],"{{site_sid}}")
                    else:
                        data_sid = data

                    data_LX_WXSRF_JTOKEN = re.findall(".*LX-WXSRF-JTOKEN=(.*?)'",data_sid)
                    if len(data_LX_WXSRF_JTOKEN) != 0:
                        data_LX_WXSRF_JTOKEN = data_sid.replace(data_LX_WXSRF_JTOKEN[0], "{{site_LX_WXSRF_JTOKEN}}")
                    else:
                        data_LX_WXSRF_JTOKEN = data_sid

                    data_laravel_session = re.findall(".*LX-WXSRF-JTOKEN=(.*?)'",data_LX_WXSRF_JTOKEN)
                    if len(data_LX_WXSRF_JTOKEN) != 0:
                        data_laravel_session = data_LX_WXSRF_JTOKEN.replace(data_laravel_session[0], "{{site_laravel_session}}")
                    else:
                        data_laravel_session = data_LX_WXSRF_JTOKEN

                    sql = 'update fusion_generate_case set headers="{}" where id={}'.format(data_laravel_session, header[0])
                    logger.info(sql)
                    my_custom_sql(sql)
            return ApiResponse(msg="清洗完成")
        except:
            return ApiResponse(msg="清洗失败",status=1)

class SummaryCaseApiView(APIView):
    def get(self,request):
        """
        每日汇报用例情况
        :return:
        """
        current_date = datetime.now().strftime('%Y-%m-%d')
        sql='select ' \
                'count(*) ' \
            'from ' \
                'fusion_generate_case_name ' \
            'where ' \
                'convert(create_time,DATETIME)  like "{}%" union all ' \
            'select ' \
                'count(*) ' \
            'from ' \
                'fusion_generate_case_name union all ' \
            'select ' \
                'count(*) from fusion_generate_case ' \
            'where  ' \
                'convert(create_time,DATETIME)  like "{}%" union all ' \
            'select ' \
                'count(*) ' \
            'from ' \
                'fusion_generate_case;'.format(current_date,current_date)
        data_result = my_custom_sql(sql)
        #结果1:当日新增用例数量
        #结果2:当日用例中新增接口数量
        #结果3:总共用例数量
        #结果4:总共用例中接口数量
        message = "*******每日自动化情况*******\n" \
                  "当日新增用例数量:{}\n" \
                  "当日用例中新增接口数量:{}\n" \
                  "总共用例数量:{}\n" \
                  "总共用例中接口数量:{}".format(data_result[0][0],data_result[2][0],data_result[1][0],data_result[3][0])
        # DingDing().get_message(message)
        return ApiResponse(msg="用例汇总完成")







