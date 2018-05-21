
from app import create_app

__author__ = 'KeithTt'

app = create_app()

if __name__ == '__main__':
    # 使用类方法run()启动web服务器，开启调试模式
    # 默认是以单进程单线程的方式在相应客户端的请求，开启多线程（还是单进程）
    # 多进程 processes = 1
    app.run(host='0.0.0.0', port=8088, debug=app.config['DEBUG'], threaded=True)