# LocalStack线程隔离的特性
# 使用线程隔离的意义在于：使当前线程能够正确引用到他自己所创建的对象，而不是引用到其他线程所创建的对象

from werkzeug.local import LocalStack
import threading
import time

my_stack = LocalStack()
my_stack.push(1)
print('In main thread after push, value is ' + str(my_stack.top))

def worker():
    # 由于线程隔离，这里新线程取不到主线程的栈顶元素
    print('In new thread before push, value is ' + str(my_stack.top))
    my_stack.push(2)
    # 新线程的栈顶元素将是2
    print('In new thread after push, value is ' + str(my_stack.top))

new_t = threading.Thread(target=worker, name='kt_thread')
new_t.start()

time.sleep(1)
# 主线程的栈顶元素依然是1
print('Finally, in main thread value is: ' + str(my_stack.top))

# In main thread after push, value is 1
# In new thread before push, value is None
# In new thread after push, value is 2
# Finally, in main thread value is: 1
