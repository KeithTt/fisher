from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)  # 整数类型，设置为主键，自增长
    title = Column(String(50), nullable=False)  # 字符串类型，长度为50，不能为空
    author = Column(String(30), default='未名')  # 作者，设置一个默认名字
    binding = Column(String(20))  # 装帧类型，精装还是平装
    publisher = Column(String(50))  # 出版社
    price = Column(String(20))  # 价格
    pages = Column(Integer)  # 页数
    pubdate = Column(String(20))  # 出版时间
    isbn = Column(String(20), nullable=False, unique=True)  # ISBN不能为空，必须唯一
    summary = Column(String(1000))  # 简介
    image = Column(String(50))  # 图片
