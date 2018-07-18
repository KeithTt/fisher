# 线程隔离

import threading
import time


class A:
    b = 1

my_obj = A()

def worker():
    my_obj.b = 2

new_t = threading.Thread(target=worker, name='kt_thread')
new_t.start()

# 停顿1秒，等待新线程执行完成
time.sleep(1)

# 由于并不是线程隔离的，这里会打印出新线程执行的结果
print(my_obj.b)
