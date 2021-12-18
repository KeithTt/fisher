from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.base import db
from app.models.user import User
from . import web
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.libs.email import send_mail


@web.route(rule='/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(formdata=request.form)  # 获取POST提交的表单信息 request.form
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)  # form.data 包含表单上传的所有数据
            db.session.add(user)
        return redirect(location=url_for('web.login'))  # 注册成功之后跳转到登陆页面
    return render_template('auth/register.html', form=form)  # 返回注册页面


@web.route(rule='/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(formdata=request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user=user, remember=True)  # remember参数表示记住cookie信息，默认保存时间是365天。默认情况下cookie是一次性的，即关闭浏览器就消失
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(location=next)  # 登陆成功后跳转返回到之前的页面
        else:
            flash(message='账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route(rule='/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(formdata=request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            send_mail(to=form.email.data, subject='重置密码', template='email/reset_password.html', user=user, token=user.generate_token())
            flash(message='一封邮件已发送到您的邮箱 {} 请查收邮件进行重置密码操作'.format(account_email))
            return redirect(location=url_for('web.index'))
    return render_template('auth/forget_password_request.html', form=form)


@web.route(rule='/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(formdata=request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token=token, new_password=form.password1.data)  # 更新密码
        if success:
            flash(message='密码重置成功，请使用新密码登陆')
            return redirect(location=url_for('web.login'))
        else:
            flash(message='密码重置失败')
    return render_template('auth/forget_password.html', form=form)


@web.route(rule='/logout')
def logout():
    logout_user()
    return redirect(location=url_for('web.index'))
