Flask web 项目，服务端渲染。

### 启动项目

数据源调用的外部API，处理之后的数据存入了数据库。

启动服务之前需要先安装MySQL，并确保服务能连上。

```shell
pip3 install -r requirements.txt
bash startup.sh
```

访问 `http://ip:8088/`