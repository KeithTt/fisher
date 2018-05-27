# 使用wtforms校验参数是否合规

# 至少要有一个字符，长度限制
# q = request.args['q']
# 正整数，最大值限制
# page = request.args['page']

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


# 继承Form基类
class SearchForm(Form):
    # 校验q的长度
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    # 校验page是否为正整数
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
