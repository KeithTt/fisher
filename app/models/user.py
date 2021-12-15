from math import floor
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):
    """
    继承 flask_login 的 UserMixin 类
    """
    # __tablename__ = 'user1'  # 默认情况下，sqlalchemy 会用类名创建表名，可以使用内置属性__tablename__自定义表名
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)  # 传递一个字符串，重命名字段名
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)  # 鱼豆
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    # 属性获取 getter
    @property
    def password(self):
        return self._password

    # 属性设置 setter
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        """验证密码是否正确"""
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)  # 查询是否存在这个isbn
        if not yushu_book.first:
            return False
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()  # 不允许一个用户同时赠送多本相同的书
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()  # 对于同一本书，一个用户不可能同时成为赠送者和索要者
        return True if not gifting and not wishing else False  # 既不在赠送清单，也不在心愿清单才能添加

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False

    def generate_token(self, expiration=600):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')  # 写入用户信息到序列化器

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'])
        try:
            """token伪造或者过期会抛异常"""
            data = s.loads(s=token.encode('utf-8'))  # 读取用户信息，反序列化
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get_or_404(uid)  # 通过主键获取用户模型
            user.password = new_password  # 修改密码
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


@login_manager.user_loader
def get_user(uid):
    """通过uid返回用户模型"""
    return User.query.get_or_404(str(uid))
