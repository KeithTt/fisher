# ViewModel

# 裁剪：不需要全部字段
# 修饰：需要修改数据
# 合并：需要多种数据

# http://localhost:8088/book/search/?q=9787070511209
# http://localhost:8088/book/search/?q=红楼梦


class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = '、'.join(book['author'])
        self.image = book['image']
        self.price = book['price']
        self.summary = book['summary'] or ''
        self.pages = book['pages'] or ''
        self.isbn = book['isbn']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


class _BookViewModel:
    # 描述特征（类变量、实例变量）
    # 行为（方法）
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            # 列表推导式简化代码
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'author': '、'.join(data['author']),
            'pages': data['pages'] or '',
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return book

    # @classmethod
    # def __cut_book_data(cls, data):
    #     books = []
    #     for book in data['books']:
    #         r = {
    #             'title': data['title'],
    #             'publisher': data['publisher'],
    #             'author': '、'.join(data['author']),
    #             'pages': data['pages'],
    #             'price': data['price'],
    #             'summary': data['summary'],
    #             'image': data['image']
    #         }
    #         books.append(r)
    #     return books
