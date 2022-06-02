# -*-coding:utf-8 -*-
# __author__ = 'wuhongbin'
# Time:2021/1/26 11:21 上午
import re
from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from .models import Users
from django_redis import get_redis_connection
from utils.aesPassword import aes_decode,aes_encode
from lwjTest.settings import *
class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,label="确认密码")
    sms_code = serializers.CharField(write_only=True,label="验证码")
    token = serializers.CharField(read_only=True,label="token")

    class Meta:
        model = Users
        fields = ['id','username','mobile','password','password2','sms_code','token','email','is_staff','name']
        extra_kwargs = {  # 修改字段选项
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {  # 自定义校验出错后的错误信息提示
                    'min_length': '仅允许8-15个字符的用户名',
                    'max_length': '仅允许8-15个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                # 'min_length': 8,
                # 'max_length': 20,
                # 'error_messages': {
                #     'min_length': '仅允许8-20个字符的密码',
                #     'max_length': '仅允许8-20个字符的密码',
                # }
            }
        }

    #手机号格式效验
    def validate_mobile(self, value):
        """
        :param value:手机号
        :return:
        """
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError({"message":"手机号格式有误"})
        return value

    def validate(self, attrs):
        """
        多个字段验证
        :param attrs:
        :return:
        """
        if attrs['password']!= attrs['password2']:
            raise serializers.ValidationError({"message":"2个密码不一致"})

        #验证码效验(测试环境不发送验证码)
        redis_conn = get_redis_connection("verify_code")
        mobile = attrs['mobile']
        #redis获取验证码
        real_sms_code = redis_conn.get("sms_{}".format(mobile))
        if real_sms_code==None:
            raise serializers.ValidationError({"message":"验证码已过期"})
        # elif attrs['sms_code']!=real_sms_code.decode():
        elif attrs['sms_code']!="123456":
            raise serializers.ValidationError({"message":"验证码错误"})
        return attrs

    def create(self, validated_data):
        logger.info("validated_data:{}".format(validated_data))
        #把多余的字段去掉后储存到数据库
        # validated_data前端传的参数，格式{'username': 'xiaoxi', 'mobile': '13683450124', 'password': 'xiaoxi123', 'password2': 'xiaoxi123', 'sms_code': '212170'}
        del validated_data['password2']
        del validated_data['sms_code']
        #密码需要取出来加密后再放进去
        password = validated_data.pop('password')
        mobile = validated_data['mobile']
        user = Users(**validated_data)
        #aes解密
        aes_password = aes_decode(password, mobile)
        logger.info("解密后的密码{}".format(aes_password))
        #django的加密
        user.set_password(aes_password)
        user.save()

        # 引用jwt中的叫jwt_payload_handler函数(生成payload)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 函数引用 生成jwt

        # 根据user生成用户相关的载荷
        payload = jwt_payload_handler(user)
        # 传入载荷生成完整的jwt
        token = jwt_encode_handler(payload)
        user.token = token
        return user

    def update(self, instance, validated_data):
        """
        :param instance: 原来的值
        :param validated_data: 要更新的值
        :return:
        """
        #对密码aes解密
        aes_decode_password = aes_decode(validated_data['password'],validated_data['mobile'])
        #djang加密
        instance.username = validated_data.get('username')
        instance.set_password(aes_decode_password)
        instance.save()
        logger.info("更新成功")
        return instance






