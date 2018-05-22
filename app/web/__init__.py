
from flask import Blueprint

__author__ = 'KeithTt'

# 蓝图 blueprint，蓝图是不能独立存在的，必须要插入flask的核心对象app里，每一个蓝图又能够插入很多视图函数
# 原本是把视图函数直接注册到app核心对象

# 创建一个蓝图
web = Blueprint('web', __name__)

from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
