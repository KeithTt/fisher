
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.models.base import db, Base
from sqlalchemy.orm import relationship

class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(20), nullable=False)
    launched = Column(Boolean, default=False)