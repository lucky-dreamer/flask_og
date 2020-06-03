from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,TextAreaField,IntegerField
from wtforms.validators import DataRequired, Regexp, EqualTo,length,number_range
from flask_wtf.file import FileField,FileAllowed,FileRequired
import config
from flask_ckeditor import CKEditorField


class generate_introduce_Form(FlaskForm):  # 定义表单类
    theme = StringField('我的课题', validators=[DataRequired()])  # 类变量相应的字段，label,及验证函数..
    introduce = CKEditorField('简介',validators=[DataRequired()])
    contain = IntegerField('课程容量',validators=[DataRequired()])
    teacher_time=StringField('教师选择时间（格式：xxxx-xx-xx,请用英文输入法）（学生必须在这个时间之前完成初选）',validators=[DataRequired(),length(min=10,max=10)])
    final_time=StringField('最终截至时间（格式：xxxx-xx-xx,请用英文输入法）（学生必须在这个时间之前确定自己已经选上导师）',validators=[DataRequired(),length(min=10,max=10)])
    submit = SubmitField('生成')
#     cf_pw = PasswordField('确认密码', validators=[DataRequired(), Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[a-zA-Z0-9]{8,16}$'),
#                                               EqualTo('new_pw')])
#     phone = StringField('手机号', validators=[DataRequired(), Regexp('^1[34578]\\d{9}$')])


class Inform(FlaskForm):
    inform=FileField('请上传公告文档，大小在16M以内',validators=[FileAllowed(config.Config.ALLOWED_EXTENSIONS,'上传正确的文件类型'),FileRequired()])
    submit=SubmitField('上传')


class FileForm(FlaskForm):
    inform = FileField('请上传说明书文档，大小在16M以内',
                       validators=[FileAllowed(config.Config.ALLOWED_EXTENSIONS, '上传正确的文件类型'), FileRequired()])
    submit = SubmitField('上传')


class GradePowerForm(FlaskForm):
    daily=StringField('平时成绩', validators=[DataRequired()])
    answer=StringField('答辩成绩', validators=[DataRequired()])
    final=StringField('说明书成绩', validators=[DataRequired()])
    submit = SubmitField('确定')


class SignNumberForm(FlaskForm):
    sign_number=StringField('请输入四位数的签到码，并且告知学生用签到码进行签到',validators=[DataRequired(),length(min=4,max=4)])
    submit = SubmitField('确定')


class StudentNumberForm(FlaskForm):
    sign_number = StringField('请输入四位数的签到码进行签到', validators=[DataRequired(), length(min=4, max=4)])
    submit = SubmitField('签到')


class AskForm(FlaskForm):
    question = CKEditorField('请输入你的问题',validators=[DataRequired()])
    submit = SubmitField('提交')


class ReplyForm(FlaskForm):
    # reply = TextAreaField('发表回复',validators=[DataRequired()])
    reply=CKEditorField('发表回复',validators=[DataRequired()])
    submit = SubmitField('回复')