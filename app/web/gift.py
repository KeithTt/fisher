from flask import current_app, flash, redirect, url_for

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
    if current_user.can_save_to_list(isbn):
        # 事务
        # 回滚
        # try:
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            # current_user实际上是实例化的User模型
            gift.uid = current_user.id
            ##########################
            # 每上传一本书赠送0.5个鱼豆
            # current_user.beans += 0.5
            current_user.beans += current_app.config['BEANS_UPLODAD_ONE_BOOK']
            db.session.add(gift)
            # db.commit()
        # except Exception as e:
        #     # 如果try语句执行失败，则回滚
        #     db.session.rollback()
        #     raise e
    else:
        flash('这本书已经添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
