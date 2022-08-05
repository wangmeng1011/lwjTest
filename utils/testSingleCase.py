# -*-coding:utf-8 -*-
# Time:2020/11/12 11:33 上午
import unittest,os
from ddt import ddt,data,unpack,file_data
import unittest
import os,time
import json
from lwjTest.settings import logger
from utils.dictor import dictor
import yaml

def result_json():
    curpath = os.path.dirname(os.path.realpath(__file__))
    yamlpath = os.path.join(curpath, "response.txt")
    with open(yamlpath, "r") as f:
        result_value = f.read()
        result_json = json.loads(result_value)
    return result_json

@ddt
class TestSingleCase(unittest.TestCase):
    def setUp(self) -> None:
        print("==========================================================开始执行测试用例===============================================================")

    @data(*result_json())
    def test_single_case(self,value):
        self._testMethodName = "test_single_case"
        self._testMethodDoc = value[1]
        print("==========================================================步骤:{}==========================================================".format(1))
        print("api名称:{}".format(value[1]))
        print("请求地址:{}".format(value[2]))
        print("请求方法:{}".format(value[3]))
        print("参数:{}".format(value[4]))
        print("响应状态码:{}".format(value[5]))
        print("预期状态码:{}".format(value[6]))
        print("响应内容:{}".format(value[7]))
        print("测试结果:{}".format(value[8]))
        self.assertEqual(value[8],"pass",msg="断言失败")

    def tearDown(self) -> None:
        print(
            "==========================================================结束测试用例运行===============================================================")
# if __name__ == '__main__':
#         unittest.main()
