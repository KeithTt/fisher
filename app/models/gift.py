from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc
from app.models.base import db, Base
from sqlalchemy.orm import relationship

from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(20), nullable=False)
    # 是否被赠送出去
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 实例代表一个具体的对象
    # 类代表一种抽象的事物
    @classmethod
    def recent(cls):
        """
        按时间倒序排序
        数量限制，显示最近上传的30本书
        去重
        """
        # 链式调用
        recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
