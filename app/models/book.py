# 模型层 MVC M层

# sqlalchemy
# Flask_SQLAlchemy

# pip3 install flask-sqlalchemy

from sqlalchemy import Column, Integer, String
from app.models.base import db

class Book(Base):
    # 整数类型，设置为主键，自增长
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 字符串类型，长度为50，不能为空
    title = Column(String(50), nullable=False)
    # 作者，设置一个默认名字
    author = Column(String(30), default='未名')
    # 装帧类型，精装还是平装
    binding = Column(String(20))
    # 出版社
    publisher = Column(String(50))
    # 价格
    price = Column(String(20))
    # 页数
    pages = Column(Integer)
    # 出版时间
    pubdate = Column(String(20))
    # ISBN不能为空，必须唯一
    isbn = Column(String(20), nullable=False, unique=True)
    # 简介
    summary = Column(String(1000))
    # 图片
    image = Column(String(50))
