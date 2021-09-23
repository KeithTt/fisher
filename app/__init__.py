from flask_mail import Mail
from app.models.base import db
from flask import Flask
from flask_login import LoginManager
from app.web import web

login_manager = LoginManager()  # 登陆管理器，该插件用于管理cookie
mail = Mail()


def create_app():
    app = Flask(__name__)  # 这里的__name__决定了应用程序的根目录
    print(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)  # 调用注册函数
    db.init_app(app)  # 关联模型层到核心对象
    db.create_all(app=app)  # 把数据模型映射到数据库里去
    login_manager.init_app(app)  # 关联登录管理器到核心对象
    login_manager.login_view = 'web.login'  # 自动跳转到登陆页面
    login_manager.login_message = '请先注册登陆'  # 自定义未登录提示
    mail.init_app(app)  # 注册email插件
    return app


def register_blueprint(app):
    # 把蓝图注册到app核心对象
    app.register_blueprint(web)
