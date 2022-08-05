# -*-coding:utf-8 -*-
# Time:2021/4/23 10:18 上午
import json
import re
from urllib import parse
from .models import GenerateCase,GenerateCaseName
from lwjTest.settings import logger,UPLOAD_ROOT
from django.db import transaction
def analysis_file(file,case_name):
    """
    解析文件
    :param file: 文件
    :param case_name: 用例名称
    :return:
    """

    #保存测试用例
    caseName = GenerateCaseName.objects.create(name=case_name)
    # 解析文件
    with open(UPLOAD_ROOT + "/" + file.name, 'r') as readObj:
        harDirct = json.loads(readObj.read())
        # 获取用例数据
        requestList = harDirct['log']['entries']
        for i in range(len(requestList)):
            # 参数提取
            argumentExtract = ""
            request_data = requestList[i]['request']
            response_data = requestList[i]['response']
            logger.info("--------获取第{}条测试步骤请求相关的数据------------".format(i+1))
            # 请求地址
            url = request_data['url']
            url=parse.urlparse(url)
            #请求域名和请求接口
            host = url.scheme + "://" + url.hostname

            if url.query == "":
                path = url.path
            else:
                path = url.path + "?" + url.query
            # 请求方法
            method = request_data['method']
            try:
                # 请求类型
                if request_data['postData']['mimeType'] == "application/x-www-form-urlencoded":
                    request_type = "data"
                    data = request_data['postData']['params']
                # elif request_data['postData']['mimeType'] == "application/json;charset=UTF-8":
                else:
                    request_type = "json"
                    #空数据
                    if request_data['postData']['text']!="{}":
                        data = request_data['postData']['text']
                    else:
                        data=""
            except:
                request_type = "data"
                data = ""

            #请求头处理
            headers = str(request_data['headers'])
            #处理特殊符合
            special_str = "{'name': 'If-None-Match', 'value':"
            if special_str in headers:
                special_header = headers.split(special_str)
                special_header_1 = special_header[1].split("},",1)
                headers = special_header[0]+"{'name': 'If-None-Match', 'value':''},"+special_header_1[1]
            #处理分销系统的请求头
            if "http://o.sales-staging.liweijia.com"==host:
                #获取响应头数据
                if "/security/lv_check" in path:
                    argumentExtract=str([{"name":"sales_sid","origin":"COOKIE","format":"sid","regular":""},{"name":"sales_LX-WXSRF-JTOKEN","origin":"COOKIE","format":"LX-WXSRF-JTOKEN","regular":""}])

                data_sid = re.findall(".*sid=(.*?);", headers)
                if len(data_sid) != 0:
                    data_sid = headers.replace(data_sid[0], "{{sales_sid}}")
                else:
                    data_sid = headers

                headers = re.findall(".*LX-WXSRF-JTOKEN=(.*?)'", data_sid)
                if len(headers) != 0:
                    headers = data_sid.replace(headers[0], "{{sales_LX_WXSRF_JTOKEN}}")
                else:
                    headers = data_sid

            #处理site系统的请求头
            elif "siteadmin" in host:
                header_sid = re.findall(".*sid=(.*?);",headers)
                if len(header_sid) != 0:
                    header_sid = headers.replace(header_sid[0], "{{site_sid}}")
                else:
                    header_sid = headers

                header_LX_WXSRF_JTOKEN = re.findall(".*LX-WXSRF-JTOKEN=(.*?)'", header_sid)
                if len(header_LX_WXSRF_JTOKEN) != 0:
                    header_LX_WXSRF_JTOKEN = header_sid.replace(header_LX_WXSRF_JTOKEN[0], "{{site_LX_WXSRF_JTOKEN}}")
                else:
                    header_LX_WXSRF_JTOKEN = header_sid

                headers = re.findall(".*LX-WXSRF-JTOKEN=(.*?)'", header_LX_WXSRF_JTOKEN)
                if len(header_LX_WXSRF_JTOKEN) != 0:
                    headers = header_LX_WXSRF_JTOKEN.replace(headers[0],
                                                                        "{{site_laravel_session}}")
                else:
                    headers = header_LX_WXSRF_JTOKEN
            #处理支付系统的请求头
            elif "pay" in host:
                #自动生产参数提取
                if "/security/lv_check" in path:
                    argumentExtract=str(
                    [{"name": "pay_XSRF_TOKEN", "origin": "COOKIE", "format": "XSRF-TOKEN", "regular": ""},
                     {"name": "pay_pay_session", "origin": "COOKIE", "format": "pay_session", "regular": ""},
                     {"name": "pay_sid", "origin": "COOKIE", "format": "sid", "regular": ""},
                    {"name": "pay_LX_WXSRF_JTOKEN", "origin": "COOKIE", "format": "LX-WXSRF-JTOKEN", "regular": ""}])

                data_sid = re.findall(".*sid=(.*?);", headers)
                if len(data_sid) != 0:
                    data_sid = headers.replace(data_sid[0], "{{pay_sid}}")
                else:
                    data_sid = headers

                data_LX_WXSRF_JTOKEN = re.findall(".*LX-WXSRF-JTOKEN=(.*?);", data_sid)
                if len(data_LX_WXSRF_JTOKEN) != 0:
                    data_LX_WXSRF_JTOKEN = data_sid.replace(data_LX_WXSRF_JTOKEN[0], "{{pay_LX_WXSRF_JTOKEN}}")
                else:
                    data_LX_WXSRF_JTOKEN = data_sid

                data_LX_WXSRF_JTOKEN_1 = re.findall(".*LX-WXSRF-JTOKEN=(.*?)'", data_LX_WXSRF_JTOKEN)

                if len(data_LX_WXSRF_JTOKEN_1) != 0 and len(data_LX_WXSRF_JTOKEN_1[0]) < 50:
                    data_LX_WXSRF_JTOKEN_1 = data_LX_WXSRF_JTOKEN.replace(data_LX_WXSRF_JTOKEN_1[0],
                                                                          "{{pay_LX_WXSRF_JTOKEN}}")
                else:
                    data_LX_WXSRF_JTOKEN_1 = data_LX_WXSRF_JTOKEN

                data_pay_session = re.findall(".*pay_session=(.*?);", data_LX_WXSRF_JTOKEN_1)
                if len(data_pay_session) != 0:
                    data_pay_session = data_LX_WXSRF_JTOKEN_1.replace(data_pay_session[0], "{{pay_pay_session}}")
                else:
                    data_pay_session = data_LX_WXSRF_JTOKEN_1

                data_pay_session_1 = re.findall(".*pay_session=(.*?)'", data_pay_session)
                if len(data_pay_session_1) != 0 and len(data_pay_session_1[0]) < 50:
                    data_pay_session_1 = data_pay_session.replace(data_pay_session_1[0], "{{pay_pay_session}}")
                else:
                    data_pay_session_1 = data_pay_session

                data_XSRF_TOKEN = re.findall(".*XSRF-TOKEN=(.*?)'", data_pay_session_1)
                if len(data_XSRF_TOKEN) != 0:
                    data_XSRF_TOKEN = data_pay_session_1.replace(data_XSRF_TOKEN[0], "{{pay_XSRF_TOKEN}}")
                else:
                    data_XSRF_TOKEN = data_pay_session_1

                headers = re.findall(".*X-XSRF-TOKEN', 'value': '(.*?)'", str(data_XSRF_TOKEN))
                if len(headers) != 0:
                    headers = data_pay_session.replace(headers[0], "{{pay_X_XSRF_TOKEN}}")
                else:
                    headers = data_XSRF_TOKEN
            #处理小程序的请求头
            elif "http://cloud.sales-staging.liweijia.com"==host:
                # #判断请求头是否有Bearer
                # if "Bearer" in headers:
                #     headers="[{'name': 'Site-Key', 'value': 'huixiangjia'}, {'name': 'Store-Code', 'value': 'SFhDRFMwMg=='}, {'name': 'X-TENANT-CODE', 'value': 'o'}, {'name': 'X-Authorization', 'value': 'Bearer {{cloud_token}}'},{'name': 'LX-REQUEST-LOGIN-MODE', 'value': 'jwt'},{'name': 'Content-Type', 'value': 'application/x-www-form-urlencoded'}]"
                # else:
                #     headers="[{'name': 'Site-Key', 'value': 'huixiangjia'}, {'name': 'Store-Code', 'value': 'SFhDRFMwMg=='}, {'name': 'X-TENANT-CODE', 'value': 'o'},{'name': 'LX-REQUEST-LOGIN-MODE', 'value': 'jwt'},{'name': 'Content-Type', 'value': 'application/x-www-form-urlencoded'}]"
                #处理登录参数
                if "/security/lv_check" in path:
                    data="[{'name': 'lv_username', 'value': '13683450124'}, {'name': 'lv_password', 'value': 'liweijia666'}]"
                header_token = re.findall(".*Bearer (.*?)'", headers)
                if len(header_token) != 0:
                    header_token = headers.replace(header_token[0], "{{cloud_token}}")
                else:
                    header_token = headers

                header_sid = re.findall(".*sid=(.*?);", header_token)
                if len(header_sid) != 0:
                    header_sid = header_token.replace(header_sid[0], "{{cloud_sid}}")
                else:
                    header_sid = header_token

                headers = re.findall(".*LX-WXSRF-JTOKEN=(.*?)'", header_sid)
                if len(headers) != 0:
                    headers = header_sid.replace(headers[0], "{{cloud_LX_WXSRF_JTOKEN}}")
                else:
                    headers = header_sid

            #处理租户管理系统的请求头
            elif "admin-sales" in host:
                data_sid = re.findall(".*sid=(.*?);", headers)
                if len(data_sid) != 0:
                    data_sid = headers.replace(data_sid[0], "{{admin_sales_sid}}")
                else:
                    data_sid = headers
                headers = re.findall(".*LX-WXSRF-JTOKEN=(.*?)'", data_sid)
                if len(headers) != 0:
                    headers = data_sid.replace(headers[0], "{{admin_sales_LX_WXSRF_JTOKEN}}")
                else:
                    headers = data_sid
            #处理中转系统的请求头
            elif "oproxy-admin" in host:
                header_sid = re.findall(".*sid=(.*?);", headers)
                if len(header_sid) != 0:
                    header_sid = headers.replace(header_sid[0], "{{admin_sid}}")
                else:
                    header_sid = headers

                header_LX_WXSRF_JTOKEN = re.findall(".*LX-WXSRF-JTOKEN=(.*?)'", header_sid)
                if len(header_LX_WXSRF_JTOKEN) != 0:
                    header_LX_WXSRF_JTOKEN = header_sid.replace(header_LX_WXSRF_JTOKEN[0], "{{admin_LX_WXSRF_JTOKEN}}")
                else:
                    header_LX_WXSRF_JTOKEN = header_sid

                headers = re.findall(".*LX-WXSRF-JTOKEN=(.*?)'", header_LX_WXSRF_JTOKEN)
                if len(headers) != 0:
                    headers = header_LX_WXSRF_JTOKEN.replace(headers[0],
                                                             "{{admin_laravel_session}}")
                else:
                    headers = header_LX_WXSRF_JTOKEN
            #处理oms的请求头(租户的域名包含了oms域名的admin，所以加上了stating)
            elif "admin-staging" in host:
                #获取响应头数据
                if "/security/lv_check" in path:
                    argumentExtract=str([{"name":"oms_sid","origin":"COOKIE","format":"sid","regular":""},{"name":"oms_LX-WXSRF-JTOKEN","origin":"COOKIE","format":"LX-WXSRF-JTOKEN","regular":""}])

                data_sid = re.findall(".*sid=(.*?);", headers)
                if len(data_sid) != 0:
                    data_sid = headers.replace(data_sid[0], "{{oms_sid}}")
                else:
                    data_sid = headers

                headers = re.findall(".*LX-WXSRF-JTOKEN=(.*?)'", data_sid)
                if len(headers) != 0:
                    headers = data_sid.replace(headers[0], "{{oms_LX_WXSRF_JTOKEN}}")
                else:
                    headers = data_sid
            # 预期状态(如果是304的更新成200)
            expect_code = response_data['status']
            if expect_code==304:
                expect_code=200
            #保存测试步骤
            GenerateCase.objects.create(name=caseName,
                                            host=host,
                                            path=path,
                                            method=method,
                                            data=str(data),
                                            request_type=request_type,
                                            headers=str(headers),
                                            expect_code=expect_code,
                                            argumentExtract=argumentExtract
                                            )





