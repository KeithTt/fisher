from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo
from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空，请输入你的密码'), Length(6, 32)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少需要2个字符，最多10个字符')])

    def validate_email(self, field):
        """
        自定义验证器，必须以validate_开头，然后跟要校验的字段
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')  # 如果校验失败，则抛出校验异常

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空，请输入你的密码'), Length(6, 32)])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])


class ResetPasswordForm(Form):
    password1 = PasswordField('新密码', validators=[
        DataRequired(),
        Length(6, 20, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')
    ])
    password2 = PasswordField('确认新密码', validators=[DataRequired(), Length(6, 20)])
