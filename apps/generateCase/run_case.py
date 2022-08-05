# -*-coding:utf-8 -*-
# Time:2021/4/23 3:32 下午
import requests
import re
import os
import json
import yaml
import time
from lwjTest.settings import logger
from utils.dingDing import DingDing
from ast import literal_eval
from .models import GenerateCase,GenerateCaseName,GenerateCaseRunRecord,GenerateRunStepRecord
from .serializers import GenerateRunStepRecordSerializer
from utils.dictor import dictor
from .run_api import run_request
from apps.report.models import ReportModel
from .run_api import _replace_argument
from .data_function import DataFunction
def calculation_amount(amount_expression,global_arguments):
    """
    金额计算
    :param amount_expression: 断言表达式
    :param global_arguments: 全局参数
    :return:
    """
    if isinstance(amount_expression,str):
        if "sum" in amount_expression:
            data_expression = amount_expression.split("=")[1]
            variable_data_one = data_expression.split("+")[0]
            variable_data_two = data_expression.split("+")[1]
            data_one = float(_replace_argument(variable_data_one, global_arguments))
            data_two = float(_replace_argument(variable_data_two, global_arguments))
            logger.info("结算后的金额:{}".format(float(data_one+data_two)))
            return DataFunction().get_num(data_one+data_two)
        elif "reduce" in amount_expression:
            data_expression = amount_expression.split("=")[1]
            variable_data_one = data_expression.split("-")[0]
            variable_data_two = data_expression.split("-")[1]
            data_one = float(_replace_argument(variable_data_one, global_arguments))
            data_two = float(_replace_argument(variable_data_two, global_arguments))
            logger.info("结算后的金额:{}".format(float(data_one - data_two)))
            return DataFunction().get_num(data_one-data_two)
        elif "{{" in amount_expression:
            return DataFunction().get_num(float(_replace_argument(amount_expression, global_arguments)))
        else:
            return amount_expression
    else:
        return amount_expression


def run_case_list(case_id_list):
    """
    批量执行测试用例
    :param case_id_list:
    :return:
    """
    case_response_list = []

    for case_id in list(case_id_list):
        logger.info("执行测试用例id:{}".format(case_id))
        serializer_list = []
        # 全局参数
        global_arguments = {}

        #创建测试用例运行记录
        generateCaseName = GenerateCaseName.objects.get(pk=case_id)
        generateCaseRunRecord = GenerateCaseRunRecord.objects.create(name=generateCaseName)

        api_apis = GenerateCase.objects.filter(name_id=case_id)
        for api in api_apis:
            #运行api
            res = run_request(api=api,arguments=global_arguments,generateCaseRunId=generateCaseRunRecord)
            logger.info("cookies:--------{}".format(requests.utils.dict_from_cookiejar(res.cookies)))
            #等待时间
            time.sleep(api.sleep_time)
            #运行API后，看下是否还有参数需要提取
            if api.argumentExtract:
                api_argument_list = literal_eval(api.argumentExtract)
                for api_argument_dict in api_argument_list:
                    dictor_data = {}
                    # 请求头
                    if api_argument_dict['origin'] == 'HEAD':
                        dictor_data = res.headers
                        logger.info("headers—response:{}".format(dictor_data))
                    elif api_argument_dict['origin'] == 'COOKIE':
                        # 获取cookies返回的字典
                        dictor_data = requests.utils.dict_from_cookiejar(res.cookies)
                        logger.info("cookies-response:{}".format(dictor_data))
                        # 响应
                    elif api_argument_dict['origin'] == 'BODY':
                        dictor_data = res.json()
                        logger.info("body-response:{}".format(dictor_data))
                    argument_value = dictor(dictor_data,api_argument_dict['format'])
                    logger.info("参数提取:{}---{}".format(api_argument_dict['name'],argument_value))
                    #特殊处理，提取内容后，对内容做正则提取或者截取
                    if api_argument_dict['regular']==None or api_argument_dict['regular']=='':
                        pass
                    else:
                        argument_value = re.split(api_argument_dict['regular'],argument_value)[1]
                    global_arguments[api_argument_dict['name']] = str(argument_value)

        logger.info("全局参数:{}".format(global_arguments))

        #获取运行记录
        generateRunStepRecord = GenerateRunStepRecord.objects.filter(case=generateCaseRunRecord)
        serializer = GenerateRunStepRecordSerializer(generateRunStepRecord,many=True).data
        serializer_list.append(serializer)
        result_json = json.dumps(serializer, ensure_ascii=False)
        result_list = json.loads(result_json)
        # logger.info("result_list:{}".format(result_list))
        for i in range(len(result_list)):
            api_id = result_list[i].get("api")
            # 用例名称
            case_name = generateCaseName.name
            # 请求url
            url = result_list[i].get("url")
            # 请求方法
            method = result_list[i].get("http_method")
            # 参数
            data = result_list[i].get("data")
            #请求头
            headers = result_list[i].get("headers")
            #cookie
            cookie = result_list[i].get("cookie")
            # 预期状态码
            expect_code = GenerateCase.objects.get(pk=api_id).expect_code
            # 预期结果
            expect_content = GenerateCase.objects.get(pk=api_id).expect_content
            # 响应状态码
            return_code = int(result_list[i].get("return_code"))
            # 响应内容
            return_content = result_list[i].get("return_content")
            #响应时间
            return_time = result_list[i].get("runTime")
            #api备注
            api_remakes = GenerateCase.objects.get(pk=api_id).remarks
            #备注，主要是查看断言失败的原因
            remarks = []
            assert_code=""
            # 断言状态码
            if expect_code == return_code:
                #断言内容
                logger.info("断言数据:{}".format(result_list[i].get("expect_content")))
                if expect_content:
                    #遍历断言内容
                    for assert_content in literal_eval(expect_content):
                        actual_value = dictor(json.loads(return_content), assert_content['name'])
                        assert_value = assert_content['value']
                        assert_value = calculation_amount(assert_value,global_arguments)
                        #每个内容断言确认
                        if actual_value == assert_value:
                            assert_code = "pass"
                        else:
                            assert_code = "fail"
                            remarks.append("断言内容不一致，响应数据提取内容:{},预期内容:{},实际内容:{}".format(assert_content['name'],assert_value, actual_value))
                            logger.error("断言内容不一致，预期内容:{},实际内容:{}".format(assert_value, actual_value))
                            break
                else:
                    assert_code = "pass"
            #状态码不一致
            else:
                assert_code = "fail"
                remarks.append("状态码不一致，预期状态码:{},实际状态码:{}".format(expect_code,return_code))
                logger.error("状态码不一致，预期状态码:{},实际状态码:{}".format(expect_code,return_code))

            if assert_code=="fail":
                content="url:{}\n" \
                        "method:{}\n" \
                        "data:{}\n" \
                        "expect_code:{}\n" \
                        "expect_content:{}\n" \
                        "return_code:{}\n" \
                        "assert_code:{}\n" \
                        "return_time:{}\n" \
                        "return_content:{}\n" \
                        "remarks:{}".format(url,method,data,expect_code,expect_content,return_code,assert_code,return_time,return_content,remarks)
                DingDing().get_message(content)
            case_response_list.insert(i, [case_name, url, method, data, expect_code,expect_content,headers,cookie,return_code,return_time, return_content,assert_code,remarks,api_remakes])
    with open("utils/response.txt", "w") as f:
        f.write(json.dumps(case_response_list, ensure_ascii=False))
    os.system('python3 utils/testGenerateManySuite.py')
    curpath = os.path.dirname(os.path.realpath(__file__))  # 获取文件当前路径
    yamlpath = os.path.join(curpath, "../../utils/case.yaml")  # 获取yaml文件地址
    data = open(yamlpath, 'r')
    report_data = yaml.load(data.read(), Loader=yaml.Loader)
    ReportModel.objects.create(
        project_name=report_data['project_name'],
        project_host=report_data['project_host'],
        case_type=report_data['case_type'],
        case_all=report_data['case_all'],
        case_pass=report_data['case_pass'],
        case_fail=report_data['case_fail'],
        start_time=report_data['start_time'],
        run_time=report_data['run_time'],
        report_details=report_data['report_details']
    )
    return report_data['report_details']

def run_case_task(case_id):
    """
    定时任务调运行用例
    :param case_id:
    :return:
    """
    case_list = literal_eval(case_id)
    run_case_list(case_list)
