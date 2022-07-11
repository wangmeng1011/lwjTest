# -*-coding:utf-8 -*-
# __author__ = 'wuhongbin'
# Time:2021/2/14 1:29 上午
import os
import requests
from urllib import parse
import json
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lwjTest.settings import logger

from ast import literal_eval
from utils.dingDing import DingDing
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lwjTest.settings import logger
from utils.data_function import DataFunction

# def _replace_argument(target_str,arguments):
#     """
#     :param target_str: 原始数据
#     :param arguments: 需要替换的数据
#     :return:
#     """
#     # if type(target_str)==dict:
#     #     target_str = json.dumps(target_str)
#     # if not arguments:
#     #     return target_str
#     # while True:
#     #     search_result = re.search(r"{{(.+?)}}",target_str)
#     #     if not search_result:
#     #         break
#     #     argument_name = search_result.group(1)
#     #     if argument_name in arguments:
#     #         target_str = re.sub("{{"+argument_name+"}}",arguments[argument_name],target_str)
#     #     else:
#     #         target_str = re.sub("{{"+argument_name+"}}",argument_name,target_str)
#     # return target_str
#
#     if type(target_str)==str:
#         if not arguments:
#             return target_str
#         while True:
#             search_result = re.search(r"{{(.+?)}}",target_str)
#             if not search_result:
#                 break
#             argument_name = search_result.group(1)
#             if argument_name in arguments:
#                 target_str = re.sub("{{"+argument_name+"}}",arguments[argument_name],target_str)
#             else:
#                 target_str = re.sub("{{"+argument_name+"}}",argument_name,target_str)
#         return target_str
#     elif type(target_str)==dict:
#         target_str = json.dumps(target_str)
#         if not arguments:
#             return target_str
#         while True:
#             search_result = re.search(r"{{(.+?)}}",target_str)
#             if not search_result:
#                 break
#             argument_name = search_result.group(1)
#             if argument_name in arguments:
#                 target_str = re.sub("{{"+argument_name+"}}",arguments[argument_name],target_str)
#             else:
#                 target_str = re.sub("{{"+argument_name+"}}",argument_name,target_str)
#         return json.loads(target_str)
#     elif type(target_str)==list:
#         return target_str
#
#     elif type(target_str)==int:
#         return target_str


# def apiRequest(api,arguments=None,reset_data=None):
#     host = api.host.host
#     method = api.http_method
#     request_type = api.request_type
#     path = api.path
#     url = parse.urljoin(host, path)
#     url = _replace_argument(url,arguments)
#     logger.info("请求的url:{}".format(url))
#     #替换请求参数的变量
#     data = {}
#     #判断请求参数是否被重写
#     # if reset_data:
#     #     #重写请求参数
#     #     data_dict = json.loads(reset_data, encoding='utf-8')
#     #     for key,value in data_dict.items():
#     #         data[key] = _replace_argument(value,arguments)
#     # elif api.data:
#     #     #使用以前的请求参数
#     #     data_dict = json.loads(api.data, encoding='utf-8')
#     #     for key,value in data_dict.items():
#     #         data[key] = _replace_argument(value,arguments)
#     if reset_data:
#         #重写请求参数
#         data_list = json.loads(reset_data, encoding='utf-8')
#         for data_dict in data_list:
#             for key,value in data_dict.items():
#                 data[key] = _replace_argument(value,arguments)
#     elif api.data:
#         #使用以前的请求参数
#         data_list = json.loads(api.data, encoding='utf-8')
#         for data_dict in data_list:
#             for key,value in data_dict.items():
#                 data[key] = _replace_argument(value,arguments)
#
#     headers = {}
#     if api.headers:
#         header_list = json.loads(api.headers, encoding='utf-8')
#         for header_dict in header_list:
#             for key,value in header_dict.items():
#                 headers[key] = _replace_argument(value,arguments)
#     logger.info("headers:{}".format(headers))
#     logger.info("==============发起请求====================")
#     if request_type=="json":
#         res = requests.request(method, url, headers=headers, json=data,verify=False)
#         logger.info("==============请求结束====================")
#         logger.info("response:{}".format(res.text))
#     elif request_type=="form-data":
#         res = requests.request(method, url, headers=headers, data=data,verify=False)
#         logger.info("==============请求结束====================")
#         logger.info("response:{}".format(res.text))
#     return res


def _replace_argument(target_str,arguments):
    """
    :param target_str: 原始数据
    :param arguments: 需要替换的数据
    :return:
    """
    if type(target_str)==str:
        if not arguments:
            return target_str
        while True:
            search_result = re.search(r"{{(.+?)}}",target_str)
            if not search_result:
                break
            argument_name = search_result.group(1)
            if argument_name in arguments:
                target_str = re.sub("{{"+argument_name+"}}",str(arguments[argument_name]),target_str)
            else:
                target_str = re.sub("{{"+argument_name+"}}",argument_name,target_str)
        return target_str
    elif type(target_str)==dict:
        target_str = json.dumps(target_str)
        if not arguments:
            return target_str
        while True:
            search_result = re.search(r"{{(.+?)}}",target_str)
            if not search_result:
                break
            argument_name = search_result.group(1)
            if argument_name in arguments:
                target_str = re.sub("{{"+argument_name+"}}",arguments[argument_name],target_str)
            else:
                target_str = re.sub("{{"+argument_name+"}}",argument_name,target_str)
        return json.loads(target_str)
    elif type(target_str)==list:
        target_str = str(target_str)
        if not arguments:
            return target_str
        while True:
            search_result = re.search(r"{{(.+?)}}", target_str)
            if not search_result:
                break
            argument_name = search_result.group(1)
            if argument_name in arguments:
                target_str = re.sub("{{" + argument_name + "}}", arguments[argument_name], target_str)
            else:
                target_str = re.sub("{{" + argument_name + "}}", argument_name, target_str)
        return literal_eval(target_str)
    elif type(target_str)==int:
        return target_str
    elif type(target_str)==bool:
        return target_str
    elif type(target_str)==float:
        return target_str

def apiRequest(api,arguments=None,reset_data=None):
    host = api.host.host
    method = api.http_method
    request_type = api.request_type
    path = api.path
    url = parse.urljoin(host, path)
    url = _replace_argument(url,arguments)
    logger.info("请求的url:{}".format(url))
    #替换请求参数的变量
    data = dict()

    if api.data:
        #data请求类型的参数格式
        if request_type == "data":
            request_data_list = literal_eval(api.data)
            logger.info(request_data_list)
            for data_dict in request_data_list:
                for key, value in data_dict.items():
                    if type(value) ==str:
                        if "___" in value:
                            FUNC_EXPR = '___(.*?){(.*?)}'
                            funcs = re.findall(FUNC_EXPR, value)
                            original_data = DataFunction().data_parameterization(funcs)
                            data_value = _replace_argument(original_data, arguments)
                            data[key] = data_value
                        else:
                            data_value = _replace_argument(value, arguments)
                            data[key] = data_value
                    else:
                        data[key] = data[value]
        #json请求类型的参数格式
        elif request_type == "json":
                    data_list = json.loads(api.data, encoding='utf-8')
                    for key,value in data_list.items():
                        # data[key] = _replace_argument(value,arguments)
                        #处理参数需要使用自定义方法
                        if type(value)==str and "___" in value:
                            FUNC_EXPR = '___(.*?){(.*?)}'
                            value_1 = value.split("___")[0]
                            value_2 = "___" + value.split("___")[1]
                            funcs = re.findall(FUNC_EXPR, value_2)
                            value = DataFunction().data_parameterization(funcs)
                            value = str(value_1) + str(value)
                        #处理参数变量
                        if "{{" not in api.data:
                            data[key] = value
                        else:
                            data[key] = _replace_argument(value,arguments)
            # data_dict=json.loads(api.data)
            # if type(data_dict) == dict:
            #     for key,value in data_dict.items():
            #         #处理参数需要使用自定义方法
            #         if type(value)==str and "___" in value:
            #             FUNC_EXPR = '___(.*?){(.*?)}'
            #             funcs = re.findall(FUNC_EXPR, value)
            #             value = DataFunction().data_parameterization(funcs)
            #         #处理参数变量
            #         if "{{" not in api.data:
            #             data[key] = value
            #         else:
            #             data[key] = _replace_argument(value,arguments)
            # elif type(data_dict) == list:
            #     data = data_dict
            #     for list in data:
            #         for key,value in list:
            #             # 处理参数需要使用自定义方法
            #             if type(value) == str and "___" in value:
            #                 FUNC_EXPR = '___(.*?){(.*?)}'
            #                 funcs = re.findall(FUNC_EXPR, value)
            #                 value = DataFunction().data_parameterization(funcs)
            #             # 处理参数变量
            #             if "{{" not in api.data:
            #                 data[key] = value
            #             else:
            #                 data[key] = _replace_argument(value, arguments)
    logger.info("请求参数:{}".format(data))
    headers = {}
    if api.headers:
        header_list = json.loads(api.headers, encoding='utf-8')
        for header_dict in header_list:
            for key,value in header_dict.items():
                headers[key] = _replace_argument(value,arguments)
    # headers = {}
    # if api.headers:
    #     headers_list = literal_eval(api.headers)
    #     for headers_dict in headers_list:
    #         headers_key = headers_dict['name']
    #         headers_value = _replace_argument(headers_dict['value'], arguments)
    #         headers[headers_key] = headers_value
    logger.info("请求头:{}".format(headers))
    logger.info("==============发起请求====================")
    if request_type=="json":
        res = requests.request(method, url, headers=headers, json=data,verify=False,allow_redirects=False)
        logger.info("response:{}".format(res.text))
    elif request_type=="data":
        res = requests.request(method, url, headers=headers, params=data,verify=False,allow_redirects=False)
        logger.info("response:{}".format(res.text))
    logger.info("==============请求结束====================")
    #接口响应时间
    runTime = res.elapsed.total_seconds()
    if runTime>20:
        content="title:*******响应超时提醒********\n" \
                "url:{}\n" \
                "runTime:{}\n".format(url,runTime)
        # DingDing().get_message(content)
    # 保存运行记录
    return res,data

