from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from app.models.base import db, Base
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')  # 引入user模型 外键建立关联
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(20), nullable=False)  # Gift里面的isbn是有可能重复的
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        # 分组统计 func+group_by
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(Gift.isbn).all()
        # 上面返回的结果是一个元祖列表，这里将结果转换成字典列表
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list
