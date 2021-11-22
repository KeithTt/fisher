DEBUG = True

# 指定数据库类型和对应的驱动，以及用户名、密码、主机名、端口号、库名
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:leon4743@localhost:3306/fisher'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'randomkey'

# Email配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'keithtt@vip.qq.com'
MAIL_PASSWORD = 'tduvlgixzgwccbch'
