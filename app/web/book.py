from flask import jsonify, request, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import TradeInfo
from app.web import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookViewModel, BookCollection


# 使用蓝图注册视图函数
@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()  # 获取参数q的值
        page = form.page.data  # 获取参数page的值
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        # Messaging Flash
        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
            # result = YuShuBook.search_by_isbn(q)
            # result = BookViewModel.package_single(result, q)
        else:
            yushu_book.search_by_keyword(q, page)
            # result = YuShuBook.search_by_keyword(q, page)
            # result = BookViewModel.package_collection(result, q)

        books.fill(yushu_book, q)
        # return json.dumps(result), 200, {"content-type": "application/json"}
        # return jsonify(books.__dict__)
        # return json.dumps(books, default=lambda o: o.__dict__), 200, {"content-type": "application/json"}  # 用default参数传递一个函数序列化对象
    else:
        # return jsonify({'msg': '参数校验失败'})
        # return jsonify(form.errors)  # 使用form的errors属性返回错误信息
        flash('搜索的关键字不符合要求，请重新输入关键字')  # 使用消息闪现返回错误提示
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍的详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    # 判断用户是否登录
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()  # 查询出所有赠送者的信息
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()  # 查询出所有索要者的信息

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template(
        'book_detail.html',
        book=book,
        wishes=trade_wishes_model,
        gifts=trade_gifts_model,
        has_in_gifts=has_in_gifts,
        has_in_wishes=has_in_wishes
    )

# @web.route('/mod')
# def mod():
#     """
#     http://localhost:8088/test
#     """
#     r = {
#         'name': '',
#         'age': 18
#     }
#     # flash可以多次调用，消息闪现的将是一个列表
#     flash('Hello KeithTt', category='error')
#     flash('Hello Jerry', category='warning')
#     # 模板 HTML
#     # return jsonify(r)
#     return render_template('test4.html', data=r,)
