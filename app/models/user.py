
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash

from app.models.base import Base

__author__ = 'KeithTt'

class User(Base):
    # 默认情况下，sqlalchemy会用类名创建表名，可以使用内置方法__tablename__自定义表名
    # __tablename__ = 'user1'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    # 在方法里面传递一个字符串，自定义字段名
    _password = Column('password', String(128))
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    # 属性读取 getter
    @property
    def password(self):
        return self._password

    # 属性写入
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)
