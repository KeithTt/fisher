from flask import current_app

from app.models.base import db
from app.models.gift import Gift
from . import web
from flask_login import login_required, current_user

__author__ = 'KeithTt'


@web.route('/my/gifts')
@login_required
def my_gifts():
    """
    http://localhost:8088/my/gifts
    """
    return 'My gifts.'


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    gift = Gift()
    gift.isbn = isbn
    # current_user实际上是实例化的User模型
    gift.uid = current_user.id
    # 每上传一本书赠送0.5个鱼豆
    # current_user.beans += 0.5
    current_user.beans += current_app.config['BEANS_UPLODAD_ONE_BOOK']
    db.session.add(gift)
    db.commit()


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
