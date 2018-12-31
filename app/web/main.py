from flask import render_template

from app.models.gift import Gift
from app.view_models.book import BookViewModel
from . import web


# 首页显示最近上传的礼物
@web.route('/')
def index():
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', books=books)


@web.route('/personal')
def personal_center():
    pass
