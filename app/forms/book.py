from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp

"""
使用wtforms校验参数是否合规

至少要有一个字符，长度限制
q = request.args.get('q')

正整数，最大值限制
page = request.args.get('page')
"""


class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])  # 校验字符串q的长度
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)  # 校验页码page是否为正整数


class DriftForm(Form):
    recipient_name = StringField('收件人姓名', validators=[DataRequired(), Length(min=2, max=20, message='收件人姓名长度必须在2到20个字符之间')])
    mobile = StringField('手机号', validators=[DataRequired(), Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])
    message = StringField('留言')
    address = StringField('邮寄地址', validators=[DataRequired(), Length(min=10, max=70, message='地址还不到10个字吗？尽量写详细一些吧')])
