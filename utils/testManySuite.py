# -*-coding:utf-8 -*-
# Time:2020/12/20 11:06 下午
import unittest
from ruamel import yaml
from BeautifulReport import BeautifulReport
from lwjTest.settings import *
BASE_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import os
from utils.upload_oss import UploadOss
import datetime
# if not os.environ.get('DJANGO_SETTINGS_MODULE'):
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo3.settings')

# 第二种错误做如下设置，更新配置文件即可；
import django

django.setup()

def get_discover():
    report_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    test_suite = unittest.defaultTestLoader.discover("utils", pattern='testManyCase.py')
    result = BeautifulReport(test_suite)
    logger.info("测试报告路径：{}".format(os.path.join(BASE_PATH, 'templates/report')))
    result.report(
        # 报告文件名称，默认为report.html
        filename='fusion_report-{}'.format(report_time),
        # 测试报告展示名字
        description='fusiontest接口测试报告',
        # 报告存放路径
        report_dir=os.path.join(BASE_PATH, 'templates/report'),
        # 测试报告主题样式
        theme="theme_memories",
    )
    #将报告上传oss
    report_name = "fusion_report-{}".format(report_time) + ".html"
    project_add = os.path.join(BASE_PATH, 'templates/report')+"/fusion_report-{}".format(report_time)+".html"
    oss_file = UploadOss().oss_file(report_name,project_add)

    curpath = os.path.dirname(os.path.realpath(__file__))  # 获取文件当前路径
    yamlpath = os.path.join(curpath, "case.yaml")  # 获取yaml文件地址
    today = datetime.datetime.now().replace(microsecond=0)
    times = today - datetime.timedelta(days=0)
    data = {
        "project_name":"fusion_report-{}".format(report_time),
        "project_host":"test",
        "case_type":"接口",
        "case_all":result.testsRun,
        "case_pass":result.success_count,
        "case_fail":result.failure_count,
        "start_time":str(times),
        "run_time":result.fields['totalTime'],
        # "report_details":HOST + "/report/fusion_report-{}.html".format(report_time)
        "report_details":oss_file,
    }
    with open(yamlpath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, Dumper=yaml.RoundTripDumper,allow_unicode=True)

if __name__ == '__main__':
    get_discover()