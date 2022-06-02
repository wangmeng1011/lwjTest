# -*-coding:utf-8 -*-
# __author__ = 'wuhongbin'
# Time:2021/4/23 2:29 下午
import os
import requests
from urllib import parse
import json
import re
from ast import literal_eval
from utils.dingDing import DingDing
from .models import GenerateRunStepRecord
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lwjTest.settings import logger
from .data_function import DataFunction

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

def run_request(api,arguments=None,generateCaseRunId=None):
    host = api.host
    method = api.method
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
            for data_dict in request_data_list:
                data_key = data_dict['name']
                original_data = data_dict['value']
                # #处理参数需要使用自定义方法
                if "___" in original_data:
                    FUNC_EXPR = '___(.*?){(.*?)}'
                    funcs = re.findall(FUNC_EXPR, original_data)
                    original_data = DataFunction().data_parameterization(funcs)
                data_value = _replace_argument(original_data,arguments)
                data[data_key] = data_value
        #json请求类型的参数格式
        elif request_type == "json":
            data_dict=json.loads(api.data)
            if type(data_dict) == dict:
                for key,value in data_dict.items():
                    #处理参数需要使用自定义方法
                    if type(value)==str and "___" in value:
                        FUNC_EXPR = '___(.*?){(.*?)}'
                        funcs = re.findall(FUNC_EXPR, value)
                        value = DataFunction().data_parameterization(funcs)
                    #处理参数变量
                    if "{{" not in api.data:
                        data[key] = value
                    else:
                        data[key] = _replace_argument(value,arguments)
            elif type(data_dict) == list:
                data = data_dict
                for list in data:
                    for key,value in list:
                        # 处理参数需要使用自定义方法
                        if type(value) == str and "___" in value:
                            FUNC_EXPR = '___(.*?){(.*?)}'
                            funcs = re.findall(FUNC_EXPR, value)
                            value = DataFunction().data_parameterization(funcs)
                        # 处理参数变量
                        if "{{" not in api.data:
                            data[key] = value
                        else:
                            data[key] = _replace_argument(value, arguments)

    logger.info("请求参数:{}".format(data))

    headers = {}
    if api.headers:
        headers_list = literal_eval(api.headers)
        for headers_dict in headers_list:
            headers_key = headers_dict['name']
            headers_value = _replace_argument(headers_dict['value'], arguments)
            headers[headers_key] = headers_value
    logger.info("请求头:{}".format(headers))
    logger.info("==============发起请求====================")
    if request_type=="json":
        res = requests.request(method, url, headers=headers, json=data,verify=False,allow_redirects=False)
        logger.info("response:{}".format(res.text))
    elif request_type=="data":
        #根据Content-Type判断是否是上传文件接口
        if "services/upload/order" and "api/attachment/content" not in url:
            res = requests.request(method, url, headers=headers, data=data,verify=False,allow_redirects=False)
            logger.info("response:{}".format(res.text))
        else:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            files = {"file": ("2.jpg", open(BASE_DIR+"/../file/2.jpg", "rb"), "image/jpeg")}
            res = requests.request(method, url, headers=headers, files=files,data=data,verify=False,allow_redirects=False)
            logger.info("response:{}".format(res.text))
    logger.info("==============请求结束====================")

    #过滤非正常格式的接口数据
    if "<!DOCTYPE html>" in res.text:
        return_content=""
    else:
        return_content=res.text

    #接口响应时间
    runTime = res.elapsed.total_seconds()
    if runTime>20:
        content="title:*******响应超时提醒********\n" \
                "url:{}\n" \
                "runTime:{}\n".format(url,runTime)
        # DingDing().get_message(content)
    # 保存运行记录
    GenerateRunStepRecord.objects.create(
        url = url,
        http_method = method,
        data = data,
        headers = headers,
        runTime = runTime,
        return_code = res.status_code,
        return_content = return_content,
        return_cookies = requests.utils.dict_from_cookiejar(res.cookies),
        return_headers = res.headers,
        case = generateCaseRunId,
        api = api
    )
    return res




