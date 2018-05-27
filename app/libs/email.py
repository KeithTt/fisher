# pip3 install flask-mail

from flask import current_app, render_template
from flask_mail import Message

from app import mail

__author__ = 'KeithTt'


def send_mail(to, subject, template, **kwargs):
    # msg = Message('测试邮件', sender='KeithTt@vip.qq.com', body='Flask Test', recipients=['KeithTt@vip.qq.com'])
    msg = Message('[鱼书]' + ' ' + subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    mail.send(msg)
