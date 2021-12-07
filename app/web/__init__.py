from flask import Blueprint, render_template

# 蓝图 blueprint，蓝图是不能独立存在的，必须要插入flask的核心对象app里，每一个蓝图又能够插入很多视图函数

web = Blueprint(name='web', import_name=__name__)  # 创建一个蓝图


@web.app_errorhandler(404)
def page_not_found(e):
    """监控所有404异常，并返回指定页面"""
    return render_template('404.html'), 404


@web.app_errorhandler(500)
def internal_server_error(e):
    """监控所有500异常，并返回指定页面"""
    return render_template('500.html'), 500


from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
