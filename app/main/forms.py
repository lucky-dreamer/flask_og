from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Regexp, EqualTo


# class ChangeFile_Form(FlaskForm):                            # 定义表单类
#     old_pw = PasswordField('原密码', validators=[DataRequired()])  # 类变量相应的字段，label,及验证函数..
#     new_pw = PasswordField('新密码（必须为8到16位的数字字母组合）', validators=[DataRequired(),
#                            Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{8,16}$')])  # 8到16位的数字字母组合
#     cf_pw = PasswordField('确认密码', validators=[DataRequired(), Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{8,16}$'),
#                                               EqualTo('new_pw')])
#     phone = StringField('手机号', validators=[DataRequired(), Regexp('^1[34578]\\d{9}$')])
#     submit = SubmitField('提交')
