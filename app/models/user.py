# pip3 install flask_login

from math import floor
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from fisher.app import login_manager
from fisher.app.libs.enums import PendingStatus
from fisher.app.libs.helper import is_isbn_or_key
from fisher.app.models.base import Base, db
from flask_login import UserMixin

from fisher.app.models.drift import Drift
from fisher.app.models.gift import Gift
from fisher.app.models.wish import Wish
from fisher.app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):
    # 默认情况下，sqlalchemy会用类名创建表名，可以使用内置方法__tablename__自定义表名
    # __tablename__ = 'user1'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    # 在方法里面传递一个字符串，重命名字段名
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    # 鱼豆
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

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()
        # success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=2).count()
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False

    # 验证密码是否正确
    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # 返回一个可以表示用户身份的字段，这个方法包含在UserMixin里面
    # def get_id(self):
    #     return self.id

    def can_save_to_list(self, isbn):
        # 检查isbn是否符合规范
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        # 查询API中是否存在这个isbn
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 不允许一个用户同时赠送多本相同的书
        # 对于同一本书，一个用户不可能同时成为赠送者和索要者
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        # 既不在赠送清单，也不在心愿清单才能添加
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # 写入用户信息到序列化器 二进制解码为普通字符串
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        # 读取用户信息 反序列化
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        # 执行修改密码
        with db.auto_commit():
            # 通过主键获取用户模型
            user = User.query.get(uid)
            user.password = new_password
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


# 通过uid返回用户模型
@login_manager.user_loader
def get_user(uid):
    return User.query.get(str(uid))
