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
    Base_URL = 'https://app.cloopen.com:8883'

    def __init__(self):
        self.ACCOUNT_SID = config['ACCOUNT_SID']
        self.AUTH_TOKEN = config['AUTH_TOKEN']
        self.APPID = config['APPID']

    def get_request_url(self, sig):
        # https://app.cloopen.com:8883/2013-12-26/Accounts/{accountSid}/SMS/{funcdes}?sig={SigParameter}
        self.url = self.Base_URL + \
            '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s' % (
                self.ACCOUNT_SID, sig)
        return self.url

    def get_time_stamp(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def get_sigPara(self, time_stamp):
        p = hashlib.md5()
        s = self.ACCOUNT_SID+self.AUTH_TOKEN+time_stamp
        p.update(s.encode())
        return p.hexdigest().upper()

    def get_request_header(self, time_stamp):
        s = self.ACCOUNT_SID+':'+time_stamp
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            # 'Content-Length':'',
            'Authorization': base64.b64encode(s.encode()).decode()
        }
        return header

    def get_request_body(self, phone, code):
        return {
            'to': phone,
            'appId': self.APPID,
            'templateId': 1,
            'datas': [code, 3]
        }

    def request_api(self, url, header, body):
        res = requests.post(url, headers=header, data=body)
        return res.text

    def run(self, phone, code):
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
