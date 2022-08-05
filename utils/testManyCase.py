# -*-coding:utf-8 -*-
# Time:2020/11/12 11:33 上午
import unittest,os
from ddt import ddt,data,unpack,file_data
import unittest
from django.db import connection
import os

import json
os.environ['DJANGO_SETTINGS_MODULE'] = 'testPlatForm.settings'
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

    @data(*result_json)
    def test_many_case(self,value):
        self._testMethodName = "test_many_case"
        for step in range(len(value)):
            self._testMethodDoc = value[step][0]
            print("==========================================================步骤:{}==========================================================".format(step + 1))
            print("api名称:{}".format(value[step][1]))
            print("请求地址:{}".format(value[step][2]))
            print("请求方法:{}".format(value[step][3]))
            print("参数:{}".format(value[step][4]))
            print("响应状态码:{}".format(value[step][5]))
            print("预期状态码:{}".format(value[step][6]))
            print("响应内容:{}".format(value[step][7]))
            print("测试结果:{}".format(value[step][8]))
            self.assertEqual(value[step][8],"pass",msg="断言失败")

    def tearDown(self) -> None:
        print("==========================================================结束测试用例运行===============================================================")
if __name__ == '__main__':
    unittest.main()
