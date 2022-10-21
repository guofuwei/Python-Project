'''
Author: hanshan-server 2625406970@qq.com
Date: 2022-10-10 12:58:14
LastEditors: hanshan-server 2625406970@qq.com
LastEditTime: 2022-10-21 05:24:09
FilePath: /Python-Project/backend/tools/sms.py
Description: 发送短信验证码

Copyright (c) 2022 by hanshan-server 2625406970@qq.com, All Rights Reserved. 
'''

import hashlib
import datetime
import base64
import requests
import json

config = {
    # 发送短信
    'ACCOUNT_SID': '8aaf07087b52c64e017b54d412cf00bb',
    'AUTH_TOKEN': 'b1706e197a4b41c5bc87861217f96086',
    'APPID': '8aaf07087b52c64e017b54d413c700c2',
}


class Yuntongxin():
    """短信验证码
    """
    Base_URL = 'https://app.cloopen.com:8883'

    def __init__(self):
        """保存config
        """
        self.ACCOUNT_SID = config['ACCOUNT_SID']
        self.AUTH_TOKEN = config['AUTH_TOKEN']
        self.APPID = config['APPID']

    def get_request_url(self, sig):
        """获取请求的url

        Args:
            sig (string): 签名

        Returns:
            string: 生成的url
        """
        # https://app.cloopen.com:8883/2013-12-26/Accounts/{accountSid}/SMS/{funcdes}?sig={SigParameter}
        self.url = self.Base_URL + \
            '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s' % (
                self.ACCOUNT_SID, sig)
        return self.url

    def get_time_stamp(self):
        """获取时间戳
        """
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def get_sigPara(self, time_stamp):
        """生成签名参数
        """
        p = hashlib.md5()
        s = self.ACCOUNT_SID+self.AUTH_TOKEN+time_stamp
        p.update(s.encode())
        return p.hexdigest().upper()

    def get_request_header(self, time_stamp):
        """获取请求头
        """
        s = self.ACCOUNT_SID+':'+time_stamp
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            # 'Content-Length':'',
            'Authorization': base64.b64encode(s.encode()).decode()
        }
        return header

    def get_request_body(self, phone, code):
        """获取请求体
        """
        return {
            'to': phone,
            'appId': self.APPID,
            'templateId': 1,
            'datas': [code, 3]
        }

    def request_api(self, url, header, body):
        """发送请求
        """
        res = requests.post(url, headers=header, data=body)
        return res.text

    def run(self, phone, code):
        """启动过
        """
        time_stamp = self.get_time_stamp()
        sig = self.get_sigPara(time_stamp)
        url = self.get_request_url(sig)
        # print(url)
        header = self.get_request_header(time_stamp)
        body = self.get_request_body(phone, code)
        ret = self.request_api(url, header, json.dumps(body))
        return ret


if __name__ == '__main__':
    yuntongxin = Yuntongxin()
    ret = yuntongxin.run('17855997263', '123456')
    print(ret)
