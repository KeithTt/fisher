# ViewModel

# 裁剪：不需要全部字段
# 修饰：需要修改数据
# 合并：需要多种数据

# http://localhost:8088/book/search/?q=9787070511209
# http://localhost:8088/book/search/?q=红楼梦


class BookViewModel:
    """
    处理单本书
    """
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
    """
    集合多本书
    """
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]
