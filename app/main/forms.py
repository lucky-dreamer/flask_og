from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,TextAreaField,IntegerField
from wtforms.validators import DataRequired, Regexp, EqualTo,length


class generate_introduce_Form(FlaskForm):# 定义表单类
    theme = StringField('我的课题', validators=[DataRequired()])  # 类变量相应的字段，label,及验证函数..
    introduce = TextAreaField('简介',validators=[DataRequired()])
    contain = IntegerField('课程容量',validators=([DataRequired()]))
    teacher_time=StringField('教师选择时间（格式：xxxx-xx-xx,请用英文输入法）（学生必须在这个时间之前完成初选）',validators=[DataRequired(),length(min=10,max=10)])
    final_time=StringField('最终截至时间（格式：xxxx-xx-xx,请用英文输入法）（学生必须在这个时间之前确定自己已经选上导师）',validators=[DataRequired(),length(min=10,max=10)])
    submit = SubmitField('生成')
#     cf_pw = PasswordField('确认密码', validators=[DataRequired(), Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{8,16}$'),
#                                               EqualTo('new_pw')])
#     phone = StringField('手机号', validators=[DataRequired(), Regexp('^1[34578]\\d{9}$')])
