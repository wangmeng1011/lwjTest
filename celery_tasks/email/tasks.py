# -*-coding:utf-8 -*-
# Time:2021/2/5 10:47 上午
from celery_tasks.main import celery_app
from django.core.mail import send_mail
from django.conf import settings
@celery_app.task(name='send_verify_email')
def send_verify_email(to_email):
    """
    发激活邮箱的邮件
    :param to_email: 收件人邮箱
    :return:
    """

    subject = "测试邮箱验证"  # 邮件主题/标题
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="https://www.baidu.com">百度<a></p>' % (to_email)
    # send_mail(subject:标题, message:普通邮件正文, 发件人, [收件人], html_message=超文本的邮件内容)
    send_mail(subject, '', settings.EMAIL_FROM, [to_email], html_message=html_message)
