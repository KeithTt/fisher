# 打印书名，自动在前后加上书名号

from contextlib import contextmanager

@contextmanager
def book_mark():
    print('《', end='')
    yield
    print('》')

with book_mark():
    print('且将生活一饮而尽', end='')
