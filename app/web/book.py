
from flask import jsonify, request, render_template, flash
from app.forms.book import SearchForm
from app.web import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookViewModel, BookCollection
import json

# 使用蓝图注册视图函数
@web.route('/book/search/')
def search():
    '''
    http://localhost:8088/book/search/?q=红楼梦&page=1
    '''
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        # 获取参数q的值
        q = form.q.data.strip()
        # 获取参数page的值
        page = form.page.data
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
        # 这里直接返回的result是一个字典，用json.dumps()序列化这个字典转变为json格式，并指定状态码和content-type
        # return json.dumps(result), 200, {"content-type": "application/json"}
        # return jsonify(books.__dict__)
        return json.dumps(books, default=lambda o: o.__dict__), 200, {"content-type": "application/json"}

    else:
        # return jsonify({'msg': '参数校验失败'})
        # 使用form的errors属性返回错误信息
        return jsonify(form.errors)


@web.route('/test')
def test():
    '''
    http://localhost:8088/test
    '''
    r = {
        'name': '',
        'age': 18
    }
    # 模板 HTML
    # return jsonify(r)
    return render_template('test4.html', data=r,)
