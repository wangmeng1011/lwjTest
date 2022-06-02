# -*-coding:utf-8 -*-
# __author__ = 'wuhongbin'
# Time:2021/5/21 2:37 下午
import random
import re
import json
import datetime
import hashlib
import string
from faker import Faker
from decimal import Context,ROUND_HALF_UP


class DataFunction():
    fake = Faker(locale='zh_CN')

    def md5(self, key):
        """
        md5加密
        :param key:
        :return:
        """
        result = hashlib.md5()
        result.update(key.encode("utf-8"))
        result_code = result.hexdigest()
        return result_code.lower()

    def randomstr(self, length):
        '''
        生成指定长度大小写字母组合
        :param length:
        :return:
        '''
        return ''.join(random.sample(string.ascii_letters, length)).lower()

    def randomstrInt(self, length):
        '''
        生成指定长度随机数字和大小写字母组合
        :param length:
        :return:
        '''
        return ''.join(random.sample(string.ascii_letters + string.digits, length)).lower()

    def randomint(self, length):
        '''
        生成指定长度随机数字
        :param length:
        :return:
        '''
        s = [str(i) for i in range(10)]
        return ''.join(random.sample(s, length))

    def randomWord(self, length):
        """
        生成指定长度随机汉字
        :param length:
        :return:
        """
        str_data = ""
        for i in range(length):
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xfe)
            val = f'{head:x} {body:x}'
            str = bytes.fromhex(val).decode('gb2312')
            str_data = ''.join([str_data, str])
        return str_data

    def times(self, day):
        """
        获取时间
        :param day: day<0：未来时间，day>0：过去时间
        :return:
        """
        today = datetime.datetime.now().replace(microsecond=0)
        times = today - datetime.timedelta(days=day)
        return str(times)

    def phone_number(self):
        """
        生成随机手机号码
        :return:手机号码
        """
        return self.fake.phone_number()

    def email(self, *args, **kwargs):
        """
        生成随机邮箱
        :return:邮箱
        """
        return self.fake.email(*args, **kwargs)

    def data_parameterization(self, funcs):
        """

        :param funcs:
        :return:
        """
        if funcs[0][0] == "md5":
            original_data = self.md5(funcs[0][1])
        elif funcs[0][0] == "str":
            original_data = self.randomstr(int(funcs[0][1]))
        elif funcs[0][0] == "int":
            original_data = self.randomint(int(funcs[0][1]))
        elif funcs[0][0] == "str_int":
            original_data = self.randomstrInt(int(funcs[0][1]))
        elif funcs[0][0] == "word":
            original_data = self.randomWord(int(funcs[0][1]))
        elif funcs[0][0] == "times":
            original_data = self.times(int(funcs[0][1]))
            print(original_data)
        elif funcs[0][0] == "phone":
            original_data = self.phone_number()
        elif funcs[0][0] == "email":
            print(funcs[0][1])
            if len(funcs[0][1]) is None:
                original_data = self.email()
            else:
                original_data = self.email((funcs[0][1]))
        elif funcs[0][0] == "randomstrInt":
            original_data = self.randomstrInt(int(funcs[0][1]))
        return original_data

    def get_num(self,num):
        """
        处理精度丢失
        :param num:
        :return:
        """
        num = str(num)
        if float(num)>=1:
            a = "%.2f" % float(num)
            c = Context(prec=(len(a)-1), rounding=ROUND_HALF_UP).create_decimal(num)
            return float(str(c))
        if float(num)<1:
            d = float(num)*100
            if d-int(d)<0.5:
                return float(int(d)/100)
            else:
                i = (int(d)+1)/100
                return float(i)
if __name__ == '__main__':
    pass
    # print(DataFunction().data_parameterization(funcs))
    # print(DataFunction().data_parameterization(funcs))
    # print(DataFunction().email())
    # print(DataFunction().times(-2))
    # # original_data="___md5{5}"
    # # original_data="___str{5}"
    # original_data = "___int{5}"
    #     # 处理参数需要使用自定义方法
    # from utils.primordial_sql import my_custom_sql
    # sql="select data from fusion_generate_case where id=3238;"
    # data=my_custom_sql(sql)[0][0]
    # data_dict = json.loads(data)
    # data1=dict()
    # for key, value in data_dict.items():
    #     print(key,value)
    #     # 处理参数需要使用自定义方法
    #     if type(value)==str and "___" in value:
    #         FUNC_EXPR = '___(.*?){(.*?)}'
    #         funcs = re.findall(FUNC_EXPR, value)
    #         if funcs[0][0] == "md5":
    #             value = DataFunction().md5(funcs[0][1])
    #         elif funcs[0][0] == "str":
    #             value = DataFunction().randomstr(int(funcs[0][1]))
    #         elif funcs[0][0] == "int":
    #             value = DataFunction().randomint(int(funcs[0][1]))
    #         elif funcs[0][0] == "str_int":
    #             value = DataFunction().randomstrInt(int(funcs[0][1]))
    #         print(value)
    #     if "{{" not in data:
    #         data1[key] = value
    # print(data1)
