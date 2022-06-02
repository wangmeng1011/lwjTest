# -*-coding:utf-8 -*-
# __author__ = 'wuhongbin'
# Time:2020/11/12 11:33 上午
import unittest,os
from lwjTest.settings import logger
from ddt import ddt,data,unpack,file_data
import unittest
from django.db import connection
import os

import json
os.environ['DJANGO_SETTINGS_MODULE'] = 'lwjTest.settings'
def my_custom_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

curpath = os.path.dirname(os.path.realpath(__file__))
yamlpath = os.path.join(curpath, "response.txt")
with open(yamlpath, "r") as f:
    result_value = f.read()
    result_json=json.loads(result_value)


@ddt
class TestManyCase(unittest.TestCase):
    def setUp(self) -> None:
        print("==========================================================开始执行测试用例===============================================================")
        logger.info("==========================================================开始执行测试用例===============================================================")

    @data(*result_json)
    def test_many_case(self,value):
        # self._testMethodName = "test_generate_many_case"
        if value[13]:
            self._testMethodName = value[13]+"----"+value[1]
        else:
            self._testMethodName = value[1]
        # self._testMethodName = value[1]
        self._testMethodDoc = value[0]
        print("请求地址:{}".format(value[1]))
        print("请求方法:{}".format(value[2]))
        print("参数:{}".format(value[3]))
        print("预期状态码:{}".format(value[4]))
        print("预期内容:{}".format(value[5]))
        print("请求头:{}".format(value[6]))
        print("cookie:{}".format(value[7]))
        print("响应状态码:{}".format(value[8]))
        print(("响应时间:{}".format(value[9])))
        print("断言备注:{}".format(value[12]))
        print("响应内容:{}".format(value[10]))

        logger.info("请求地址:{}".format(value[1]))
        logger.info("请求方法:{}".format(value[2]))
        logger.info("参数:{}".format(value[3]))
        logger.info("预期状态码:{}".format(value[4]))
        logger.info("预期内容:{}".format(value[5]))
        logger.info("请求头:{}".format(value[6]))
        logger.info("cookie:{}".format(value[7]))
        logger.info("响应状态码:{}".format(value[8]))
        logger.info("接口响应时间:{}".format(value[9]))
        logger.info("断言备注:{}".format(value[12]))
        logger.info("响应内容:{}".format(value[10]))
        self.assertEqual(value[11],"pass",msg="断言失败")

    def tearDown(self) -> None:
        print("==========================================================结束测试用例运行===============================================================")
        logger.info("==========================================================结束测试用例运行===============================================================")

if __name__ == '__main__':
    unittest.main()
