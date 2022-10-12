from django.core.mail import send_mail
import random


def send_email(code, recv_mail):
    send_mail(
        subject='邮件验证码',
        message='您的验证码是'+str(code)+",该验证码3分钟内有效",
        from_email='3555970235@qq.com',
        recipient_list=[recv_mail],
        fail_silently=False
    )
