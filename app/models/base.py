
__author__ = 'KeithTt'

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger

# 实例化一个对象
db = SQLAlchemy()

# 定义一个基类模型，在基类模型里面继承db.Model，其他模型继承Base
class Base(db.Model):
    # create_time = Column('create_time', Integer)
    # 定义一个status属性控制数据是否被删除，默认为1表示不删除
    status = Column(SmallInteger, default=1)
