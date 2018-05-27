from app.forms.auth import RegisterForm, LoginForm, EmailForm
from app.models.base import db
from app.models.user import User
from . import web
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

__author__ = 'KeithTt'


@web.route('/register', methods=['GET', 'POST'])
def register():
    """
    http://localhost:8088/register
    """
    # 获取POST提交的表单信息 request.form
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            # form.data包含表单上传的所有数据
            user.set_attrs(form.data)
            db.session.add(user)
            # db.session.commit()
        # 注册成功之后跳转到登陆页面
        return redirect(url_for('web.login'))
    # 返回注册页面
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    """
    http://localhost:8088/login
    """
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 将用户身份信息写入cookie，默认情况下cookie是一次性的，即关闭浏览器就消失
            # remember参数表示记住cookie信息，默认保存时间是365天
            login_user(user, remember=True)
            # 获取next的查询参数
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            # 登陆成功后跳转返回到之前的页面
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
    return render_template('auth/forget_password_request.html')


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
