# 上下文管理器/生成器

class MyResource:
    # def __enter__(self):
    #     print('connect to resource')
    #     return self

    # def __exit__(self, exc_type, exc_value, tb):
    #     print('close resource connection')

    def query(self):
        print('query data')

# with MyResource() as r:
#     r.query()


from contextlib import contextmanager

@contextmanager
def make_resource():
    print('connect to resource')
    yield MyResource()
    print('close resource connection')

with make_resource() as r:
    r.query()
