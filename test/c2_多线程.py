# 多线程 更加充分地利用CPU的性能优势
# 异步编程
# python不能充分利用多核CPU的优势

# GIL 全局解释器锁 同一时刻只允许一个线程在解释器中运行 一定程度保证了线程安全

# 细粒度锁 程序员主动加的锁
# 粗粒度锁 解释器 GIL

# 解释器 cpython jpython
# GIL是cpython里面的实现，jpython里面没有

# 多进程 进程通信技术

# node.js 单进程 单线程
# CPU密集型程序 严重依赖CPU计算 视频解码
# IO密集型程序 查询数据库、请求网络资源、读写文件

# 对象是保存状态的地方

__author__ = 'KeithTt'

import threading
import time


def worker():
    print('I am a thread.')
    t = threading.current_thread()
    print(t.getName())
    time.sleep(10)


# 启动线程，如果是多线程，这里并不会停顿下来等待work()函数执行完
new_t = threading.Thread(target=worker, name='kt_thread')
new_t.start()
# I am a thread.
# kt_thread

# 直接调用worker函数，测试单线程，这里会停顿下来
# worker()

t = threading.current_thread()
# 打印线程名称
print(t.getName())
# print(t.name)
# MainThread
