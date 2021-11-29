from app import create_app

app = create_app()

if __name__ == '__main__':
    # 使用类方法run()启动web服务器，开启调试模式
    app.run(host='0.0.0.0', port=8088, debug=app.config['DEBUG'], threaded=True)
