from app.forms.auth import RegisterForm
from app.models.base import db
from app.models.user import User
from . import web
from flask import render_template, request

__author__ = 'KeithTt'


@web.route('/register', methods=['GET', 'POST'])
def register():
    '''
    http://localhost:8088/register
    '''
    # 获取POST提交的表单信息 request.form
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        # form.data包含表单上传的所有数据
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
    # 返回注册页面
    return render_template('auth/register.html', form={'data': {}})


@web.route('/login', methods=['GET', 'POST'])
def login():
    pass


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    pass
