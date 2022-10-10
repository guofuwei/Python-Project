from myblog.celery import app
from tools.sms import Yuntongxin


@app.task
def sendsms_celery(phone, code):
    yuntongxin = Yuntongxin()
    yuntongxin.run(phone, code)
