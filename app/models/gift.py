from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from app.models.base import db, Base
from sqlalchemy.orm import relationship
from app.spider.yushu_book import YuShuBook
from app.models.wish import Wish


# EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn'])

class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(20), nullable=False)
    # 是否被赠送出去
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        # 分组统计 func+group_by
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(Wish.isbn).all()
        # 上面返回的结果是一个元祖列表，这里将结果转换成字典列表
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 实例代表一个具体的对象
    # 类代表一种抽象的事物
    # 查询最近上传的图书
    @classmethod
    def recent(cls):
        """
        按时间倒序排序
        数量限制，显示最近上传的30本书
        去重
        """
        recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
