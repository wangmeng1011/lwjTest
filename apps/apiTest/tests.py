from django.test import TestCase
import os
# Create your tests here.


import requests
from urllib import parse
import json
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lwjTest.settings import logger
def _replace_argument(target_str,arguments):
    """

    :param target_str: {{变量}}
    :param arguments: 需要替换的数据
    :return:
    """
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

def test1():
    data_dict = {}
    data={"id":"ceshi"}
    a={"name":"test","value":"{{id}}"}
    for key,value in a.items():
        data_dict[key]=_replace_argument(value,data)
    print(data_dict)


