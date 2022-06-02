# -*-coding:utf-8 -*-
# __author__ = 'wuhongbin'
# Time:2021/2/14 1:29 上午

import requests
from urllib import parse
import json
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lwjTest.settings import logger
def _replace_argument(target_str,arguments):
    """
    :param target_str: 原始数据
    :param arguments: 需要替换的数据
    :return:
    """
    # if type(target_str)==dict:
    #     target_str = json.dumps(target_str)
    # if not arguments:
    #     return target_str
    # while True:
    #     search_result = re.search(r"{{(.+?)}}",target_str)
    #     if not search_result:
    #         break
    #     argument_name = search_result.group(1)
    #     if argument_name in arguments:
    #         target_str = re.sub("{{"+argument_name+"}}",arguments[argument_name],target_str)
    #     else:
    #         target_str = re.sub("{{"+argument_name+"}}",argument_name,target_str)
    # return target_str

    if type(target_str)==str:
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
        return target_str

    elif type(target_str)==int:
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
    data = {}
    #判断请求参数是否被重写
    # if reset_data:
    #     #重写请求参数
    #     data_dict = json.loads(reset_data, encoding='utf-8')
    #     for key,value in data_dict.items():
    #         data[key] = _replace_argument(value,arguments)
    # elif api.data:
    #     #使用以前的请求参数
    #     data_dict = json.loads(api.data, encoding='utf-8')
    #     for key,value in data_dict.items():
    #         data[key] = _replace_argument(value,arguments)
    if reset_data:
        #重写请求参数
        data_list = json.loads(reset_data, encoding='utf-8')
        for data_dict in data_list:
            for key,value in data_dict.items():
                data[key] = _replace_argument(value,arguments)
    elif api.data:
        #使用以前的请求参数
        data_list = json.loads(api.data, encoding='utf-8')
        for data_dict in data_list:
            for key,value in data_dict.items():
                data[key] = _replace_argument(value,arguments)

    headers = {}
    if api.headers:
        header_list = json.loads(api.headers, encoding='utf-8')
        for header_dict in header_list:
            for key,value in header_dict.items():
                headers[key] = _replace_argument(value,arguments)
    logger.info("headers:{}".format(headers))
    logger.info("==============发起请求====================")
    if request_type=="json":
        res = requests.request(method, url, headers=headers, json=data,verify=False)
        logger.info("==============请求结束====================")
        logger.info("response:{}".format(res.text))
    elif request_type=="form-data":
        res = requests.request(method, url, headers=headers, data=data,verify=False)
        logger.info("==============请求结束====================")
        logger.info("response:{}".format(res.text))
    return res




