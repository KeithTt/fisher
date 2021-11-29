from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from app.models.base import db, Base
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))  # 关联 user 表，将用户 id 作为外键
    isbn = Column(String(20), nullable=False)
    launched = Column(Boolean, default=False)  # 是否被赠送出去

    @property
    def book(self):
        """
        查询某个礼物对应的书籍
        """
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        """
        查询最近上传的图书
        - 按时间倒序排序
        - 数量限制，显示最近上传的30本书
        - 去重
        """
        recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        """
        根据 uid 查询用户所有的礼物
        """
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        """
        分组统计，查询出每个礼物对应的心愿数
        使用 db.session.query() 进行复杂查询
        """
        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list
