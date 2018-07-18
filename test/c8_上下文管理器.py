# 上下文管理器/生成器

class MyResource:
    def __enter__(self):
        print('connect to resource')
        return self

    # exc_type是错误类型、exc_value是错误内容、tb是错误的堆栈信息
    def __exit__(self, exc_type, exc_value, tb):
        print('close resource connection')

    def query(self):
        print('query data')

# 如果with里面的代码块执行出现错误，会先调用__exit__方法，然后
with MyResource() as r:
    r.query()


# from contextlib import contextmanager

# @contextmanager
# def make_resource():
#     print('connect to resource')
#     yield MyResource()
#     print('close resource connection')

# with make_resource() as r:
#     r.query()
