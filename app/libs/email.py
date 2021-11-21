from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_mail(to, subject, template, **kwargs):
    msg = Message('[鱼书] {}'.format(subject), sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template, **kwargs)  # HTML message
    app = current_app._get_current_object()  # 由于栈隔离，curren_app只是一个代理核心对象，新线程无法直接获取主线程的核心对象
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e
