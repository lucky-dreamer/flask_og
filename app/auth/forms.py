from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField,IntegerField,ValidationError
from wtforms.validators import DataRequired, Regexp, EqualTo,Email,NumberRange
from ..models import User

# 跟登陆相关的各种表单类

class LoginForm(FlaskForm):                            # 定义表单类.
    id=IntegerField('学号',validators=[DataRequired(),NumberRange(0,999999999999999)])
    old_pw = PasswordField('密码', validators=[DataRequired(),
                           Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{8,16}$')])  # 8到16位的数字字母组合
    remenber_me=BooleanField('记住登陆状态')
    submit = SubmitField('登陆')


class RegisterForm(FlaskForm):
    code = IntegerField('验证码',validators=[DataRequired(),NumberRange(0,9999)])
    id = IntegerField('账号（填写学号）', validators=[DataRequired(),NumberRange(0,999999999999999)])
    pw = PasswordField('密码（必须为8到16位的数字字母组合）', validators=[DataRequired(),
                           Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{8,16}$')])  # 8到16位的数字字母组合
    cf_pw = PasswordField('确认密码', validators=[DataRequired(), Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{8,16}$'),
                                              EqualTo('pw')])
    name=StringField('姓名',validators=[DataRequired()])

    submit = SubmitField('注册')

    def validate_id(self,field):
        if User.query.filter_by(id=field.data).first():
            raise ValidationError('账号已经存在')



class ChangeFile_Form(FlaskForm):                            # 定义表单类
    old_pw = PasswordField('原密码', validators=[DataRequired()])  # 类变量相应的字段，label,及验证函数..
    new_pw = PasswordField('新密码（必须为8到16位的数字字母组合）', validators=[DataRequired(),
                           Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{8,16}$')])  # 8到16位的数字字母组合
    cf_pw = PasswordField('确认密码', validators=[DataRequired(), Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{8,16}$'),
                                              EqualTo('new_pw')])
    phone = StringField('手机号', validators=[DataRequired(), Regexp('^1[34578]\\d{9}$')])
    submit = SubmitField('提交')



class Check_Code(FlaskForm):
    phone = StringField('手机号', validators=[DataRequired(), Regexp('^1[34578]\\d{9}$')])
    coder = SubmitField('点击发送验证码')


    def validate_id(self,field):
        if User.query.filter_by(id=field.data).first():
            raise ValidationError('账号已经存在')

class Forget_Form(FlaskForm):
    code = IntegerField('验证码',validators=[DataRequired(),NumberRange(0,9999)])
    pw = PasswordField('新密码（必须为8到16位的数字字母组合）', validators=[DataRequired(),
                           Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{8,16}$')])  # 8到16位的数字字母组合
    cf_pw = PasswordField('确认密码', validators=[DataRequired(), Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{8,16}$'),
                                              EqualTo('pw')])
    name=StringField('姓名',validators=[DataRequired()])

    submit = SubmitField('重置')

    def validate_id(self,field):
        if User.query.filter_by(id=field.data).first():
            raise ValidationError('账号已经存在')

class Check_Code_f(FlaskForm):
    id = IntegerField('账号（填写学号）', validators=[DataRequired(), NumberRange(0, 999999999999999)])
    coder = SubmitField('点击发送验证码')