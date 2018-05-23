
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.models.base import db
from sqlalchemy.orm import relationship

class Gift(Base):
    id = Column(Integer, primary_key=True)
    # 引入user模型 外键建立关联
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # Gift里面的isbn是有可能重复的
    isbn = Column(String(20), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)
