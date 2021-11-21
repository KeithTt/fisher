from contextlib import contextmanager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer


# 使用上下文管理器，设置自动提交事务
class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# 重写filter_by函数
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super().filter_by(**kwargs)


# 实例化一个db对象
db = SQLAlchemy(query_class=Query)


# 定义一个Base模型，在Base模型里面继承db.Model，其他模型继承Base
class Base(db.Model):
    __abstract__ = True  # 不创建Base表，让Base模型仅作为基类模型
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)  # 定义一个status属性，控制数据是否被删除，默认为1表示不删除

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        return datetime.fromtimestamp(self.create_time) if self.create_time else None

    def delete(self):
        self.status = 0
