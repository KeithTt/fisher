
__author__ = 'KeithTt'

from flask import Flask
from app.models.book import db

def create_app():
    # 实例化核心对象
    app = Flask(__name__)
    # 这里的__name__决定了应用程序的根目录
    # print(__name__)
    # 从配置文件载入配置
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    # 调用注册函数
    register_blueprint(app)
    # 关联模型层到核心对象
    db.init_app(app)
    # 把数据模型映射到数据库里去
    db.create_all(app=app)
    return app

# 把蓝图注册到app核心对象
def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
