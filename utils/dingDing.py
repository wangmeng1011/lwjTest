# -*-coding:utf-8 -*-
# Time:2020/10/22 10:01 上午
import requests,json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lwjTest.settings import DINGDING_URL
class DingDing(object):
    def __init__(self):
        pass

    def get_message(self,content):
            self.url = DINGDING_URL
            self.pagrem = {
                "msgtype": "text",
                "text": {
                    "content": content
                },
                "isAtAll": True
            }
            self.headers = {
                'Content-Type': 'application/json'
            }
            requests.post(url=self.url, data=json.dumps(self.pagrem), headers=self.headers,verify=False)

# if __name__ == '__main__':
#     DingDing().get_message("remarks:测试")
