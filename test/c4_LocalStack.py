# 使用Local()对象实现线程隔离
# Local使用字典的方式实现线程隔离
# LocalStack封装了Local，实现了一个线程隔离的栈结构

# 以线程ID号作为key的字典 -> Local -> LocalStack
# AppContext RequestContext -> LocalStack
# app(Flask核心对象) -> AppContext Request -> RequestContext
# current_app -> (LocalStack.top = AppContext top.app = Flask)
# request -> (LocalStack = RequestContext.top top.request = Request)

import threading
import time
from werkzeug.local import Local

class A:
    b = 1

# 实例化Local()
my_obj = Local()
my_obj.b = 1

def worker():
    my_obj.b = 2
    print('in new thread b is ' + str(my_obj.b))

new_t = threading.Thread(target=worker, name='kt_thread')
new_t.start()

# 停顿1秒，等待新线程执行完成
time.sleep(1)

# Local()对象是线程隔离的
print('in main thread b is ' + str(my_obj.b))
# in new thread b is 2
# in main thread b is 1
