from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_mail(to: str, subject, template, **kwargs):
    msg = Message(subject='[鱼书] {}'.format(subject), recipients=[to], sender=current_app.config['MAIL_USERNAME'], html=render_template(template, **kwargs))
    app = current_app._get_current_object()  # 由于栈隔离，这里需要获取真实的核心对象
    thr = Thread(target=send_async_email, args=[app, msg])  # 单独使用一个线程异步发送邮件
    thr.start()


def send_async_email(app, msg):
    """异步发送邮件"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e
