# -*-coding:utf-8 -*-
# __author__ = 'wuhongbin'
# Time:2021/1/26 5:07 下午
import base64
from Crypto.Cipher import AES
from lwjTest.settings import *
def aes_decode(password, key):
    """
    解密,先aes加密,再base64
    :param key:秘钥(mobile+"fusion"),超过16位去掉
    :param password:需要加密的内容
    :return:
    """
    try:
        keys=key+AES_KEY
        if len(keys)<16:
            keys_result = keys+"0"*(16-len(keys))
        elif len(keys)>16:
            keys_result = keys[0:16]
        elif len(keys)==16:
            keys_result = keys
        aes = AES.new(str.encode(keys_result), AES.MODE_ECB)  # 初始化加密器
        decrypted_text = aes.decrypt(base64.decodebytes(bytes(password, encoding='utf8'))).decode("utf8")  # 解密
        decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
    except Exception as e:
        return None
    else:
        return decrypted_text

#加密
def aes_encode(password, key):
    """
    加密,先aes加密,再base64
    :param key:秘钥(mobile+"fusion"),超过16位去掉
    :param password:需要加密的内容
    :return:
    """
    keys=key+AES_KEY
    if len(keys)<16:
        keys_result = keys+"0"*(16-len(keys))
    elif len(keys)>16:
        keys_result = keys[0:16]
    elif len(keys)==16:
        keys_result = keys
    while len(password) % 16 != 0:     # 补足字符串长度为16的倍数
        password += (16 - len(password) % 16) * chr(16 - len(password) % 16)
    password = str.encode(password)
    aes = AES.new(str.encode(keys_result), AES.MODE_ECB)  # 初始化加密器
    return str(base64.encodebytes(aes.encrypt(password)), encoding='utf8').replace('\n', '')  # 加密

# print(aes_decode("fUU1MuosKFSLGyrexygVpA==","13683450132"))
# print(aes_encode("xiaoxi123","13683450133"))
