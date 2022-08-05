# -*-coding:utf-8 -*-
# Time:2020/11/9 10:53 上午
from django.db import connection
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'lwjTest.settings'
def my_custom_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

import re
#
#处理特殊请求头
# sql = "select id,headers from fusion_generate_case"
# result = my_custom_sql(sql)
# for headers in result:
#     special_str = "{'name': 'If-None-Match', 'value':"
#     if special_str in headers[1]:
#         special_header = headers[1].split(special_str)
#         special_header_1 = special_header[1].split("},",1)
#         header = special_header[0]+"{'name': 'If-None-Match', 'value':''},"+special_header_1[1]
#         sql = 'update fusion_generate_case set headers="{}" where id={}'.format(header, headers[0])
#         print(sql)
#         my_custom_sql(sql)
#
#
#
#
# #分销
# sql = "select id,headers from fusion_generate_case"
# result = my_custom_sql(sql)
#
# for header in result:
#     # headers_str="{'name': 'Cookie', 'value': 'laravel_session=Tx9kQDTAjsmDpE383pi9aHXadmVu7dahaYXsfhnA; sid=sales_api91j18woueuipo5z68vxf4ci3.sales_api; LX-WXSRF-JTOKEN=97809faf-b3cb-46b0-8a02-57ea1ad498b7'}"
#     # headers_cookies= "{'name': 'Cookie', 'value': 'laravel_session=Tx9kQDTAjsmDpE383pi9aHXadmVu7dahaYXsfhnA; sid={{sales_sid}}; LX-WXSRF-JTOKEN={{sales_LX-WXSRF-JTOKEN}}'}"
#     # # 更新分销的cookies
#     # if headers_str in header[1]:
#     #     headers = header[1].split(headers_str)
#     #     update_headers = headers[0]+headers_cookies+headers[1]
#     #     #更新数据
#     #     sql = 'update fusion_generate_case set headers="{}" where id={}'.format(update_headers,header[0])
#     #     print(sql)
#     #     my_custom_sql(sql)
#     data=header[1]
#     data_sid = re.findall( ".*sid=(.*?);",data)
#     if len(data_sid)!=0:
#         data_sid = data.replace(data_sid[0],"{{sales_sid}}")
#     else:
#         data_sid = data
#
#     data_LX_WXSRF_JTOKEN=re.findall(".*LX-WXSRF-JTOKEN=(.*?)'",data_sid)
#     if len(data_LX_WXSRF_JTOKEN)!=0:
#         data_LX_WXSRF_JTOKEN = data_sid.replace(data_LX_WXSRF_JTOKEN[0],"{{sales_LX_WXSRF_JTOKEN}}")
#     else:
#         data_LX_WXSRF_JTOKEN=data_sid
#     sql = 'update fusion_generate_case set headers="{}" where id={}'.format(data_LX_WXSRF_JTOKEN, header[0])
#     # print(header[0],sql)
#     my_custom_sql(sql)
#
#
#
#
#
#
#
#
#
# # 更新支付系统的cookies
# sql='select id,host,headers from fusion_generate_case where host="http://pay-staging.liweijia.com"'
# result = my_custom_sql(sql)
# for i in result:
#     data=i[2]
#     #替换sid
#     data_sid=re.findall( ".*sid=(.*?);",data)
#     if len(data_sid)!=0:
#         data_sid = data.replace(data_sid[0],"{{pay_sid}}")
#     else:
#         data_sid = data
#
#     data_LX_WXSRF_JTOKEN=re.findall(".*LX-WXSRF-JTOKEN=(.*?);",data_sid)
#     if len(data_LX_WXSRF_JTOKEN)!=0:
#         data_LX_WXSRF_JTOKEN = data_sid.replace(data_LX_WXSRF_JTOKEN[0],"{{pay_LX_WXSRF_JTOKEN}}")
#     else:
#         data_LX_WXSRF_JTOKEN=data_sid
#
#     data_LX_WXSRF_JTOKEN_1=re.findall(".*LX-WXSRF-JTOKEN=(.*?)'",data_LX_WXSRF_JTOKEN)
#
#     if len(data_LX_WXSRF_JTOKEN_1)!=0 and len(data_LX_WXSRF_JTOKEN_1[0])<50:
#         data_LX_WXSRF_JTOKEN_1 = data_LX_WXSRF_JTOKEN.replace(data_LX_WXSRF_JTOKEN_1[0],"{{pay_LX_WXSRF_JTOKEN}}")
#     else:
#         data_LX_WXSRF_JTOKEN_1=data_LX_WXSRF_JTOKEN
#
#     data_pay_session=re.findall(".*pay_session=(.*?);",data_LX_WXSRF_JTOKEN_1)
#     if len(data_pay_session)!=0:
#         data_pay_session = data_LX_WXSRF_JTOKEN_1.replace(data_pay_session[0],"{{pay_pay_session}}")
#     else:
#         data_pay_session = data_LX_WXSRF_JTOKEN_1
#
#     data_pay_session_1=re.findall(".*pay_session=(.*?)'",data_pay_session)
#     if len(data_pay_session_1)!=0 and len(data_pay_session_1[0])<50:
#         data_pay_session_1 = data_pay_session.replace(data_pay_session_1[0],"{{pay_pay_session}}")
#     else:
#         data_pay_session_1 = data_pay_session
#
#     data_XSRF_TOKEN=re.findall(".*XSRF-TOKEN=(.*?)'",data_pay_session_1)
#     if len(data_XSRF_TOKEN)!=0:
#         data_XSRF_TOKEN = data_pay_session_1.replace(data_XSRF_TOKEN[0],"{{pay_XSRF_TOKEN}}")
#     else:
#         data_XSRF_TOKEN = data_pay_session_1
#
#     data_X_XSRF_TOKEN=re.findall(".*X-XSRF-TOKEN', 'value': '(.*?)'",str(data_XSRF_TOKEN))
#     if len(data_X_XSRF_TOKEN)!=0:
#         data_X_XSRF_TOKEN = data_pay_session.replace(data_X_XSRF_TOKEN[0],"{{pay_X_XSRF_TOKEN}}")
#     else:
#         data_X_XSRF_TOKEN = data_XSRF_TOKEN
#
#     sql = 'update fusion_generate_case set headers="{}" where id={}'.format(data_X_XSRF_TOKEN, i[0])
#     print(sql)
#     my_custom_sql(sql)
