from flask_login import UserMixin  # 验证用户登陆状态的模型
from . import login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask import redirect,url_for
import config
import os
import uuid  # 生成随机码的库
import pymysql
import functools
import time
from datetime import datetime  # 数据库

# 其实应该把学生和教师的基础数据抽离出来，这样教师和学生信息表有主键依赖，
# 写删除操作的时候只要删除原始的表，后面依赖的表的信息就相应删除了。基本信息永远不会删，但是管理信息会删
# 还是需要有管理员页面，防止教师在结束后没有点击结束按钮所带来的问题以及其他问题。


class Student(db.Model, UserMixin):
        __tablename__ = 'tb_student'
        id = db.Column(db.BigInteger, primary_key=True)  # 账号（写学号）
        name = db.Column(db.String(5))                    # 真实姓名
        phone = db.Column(db.String(64))  # 手机号,unique=True
        hash_password = db.Column(db.String(128), nullable=False)  # 密码
        grade=db.Column(db.String(5))       # 学生成绩
        is_sign = db.Column(db.Integer,default=0)  # 学生的签到状态
        personal_theme=db.Column(db.String(64))
        # sign_times=db.Column(db.Integer,default=0)  # 学生累计签到次数
        teacher_id = db.Column(db.BigInteger, db.ForeignKey('tb_teacher.id'))  # 学生所属教师的id
        questions = db.relationship('Question', backref='student')
        file = db.relationship('Files', backref='student',uselist=False)
        signs = db.relationship('Sign',backref='student')

# 在多端加入外键，在一端加入关系
        @property
        def password(self):
            raise ArithmeticError('密码是不可访问的')

        @password.setter
        def password(self, password):
            self.hash_password = generate_password_hash(password)

        def verify_password(self, password):
            return check_password_hash(self.hash_password, password)


class Files(db.Model, UserMixin):
    __tablename__ = 'tb_file'
    id = db.Column(db.BigInteger, primary_key=True)
    mission_url = db.Column(db.String(128))
    mission_name = db.Column(db.String(64))
    file_url = db.Column(db.String(128))  # 说明书文件的链接
    file_name = db.Column(db.String(64))
    student_id = db.Column(db.BigInteger, db.ForeignKey('tb_student.id'))


class Teacher(db.Model, UserMixin):
    __tablename__ = 'tb_teacher'
    id = db.Column(db.BigInteger, primary_key=True)  # 账号（写学号）
    name = db.Column(db.String(5))  # 真实姓名
    phone = db.Column(db.String(64))  # 教师电话,unique=True
    hash_password = db.Column(db.String(128), nullable=False)  # 密码
    students = db.relationship('Student', backref='teacher')  # 学生的老师，老师的学生们直接用关系来访问
    informs = db.relationship('Informs', backref='teacher')  # 与公告的关系
    course = db.relationship('Course', backref='teacher',uselist=False)
    sign_number= db.Column(db.String(4))  # 教师生成的签到码
    is_open_sign=db.Column(db.Integer,default=0)
    # 在多端加入外键，在一端加入关系。

    @property
    def password(self):
        raise ArithmeticError('密码是不可访问的')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)


class Course(db.Model, UserMixin):
    __tablename__ = 'tb_course'
    id = db.Column(db.BigInteger, primary_key=True)
    theme = db.Column(db.String(64), nullable=True)  # 教师课题主题
    introduction = db.Column(db.Text(1000), nullable=True)  # 教师课题简介
    contain = db.Column(db.Integer)  # 教师的课程容量
    teacher_time = db.Column(db.String(16))  # 教师选择时间
    final_time = db.Column(db.String(16))  # 教师设置的最终选择时间
    teacher_id = db.Column(db.BigInteger, db.ForeignKey('tb_teacher.id'))



class Informs(db.Model, UserMixin):
    __tablename__='tb_inform'
    title = db.Column(db.String(64))  # 通知的标题（文件名）
    url=db.Column(db.String(128),primary_key=True)  # 通知的链接
    time=db.Column(db.String(20))
    teacher_id = db.Column(db.BigInteger, db.ForeignKey('tb_teacher.id'))  # 教师的id作为这个表的外键


class Question(db.Model, UserMixin):
    __tablename__ = 'tb_question'
    id = db.Column(db.BigInteger, primary_key=True)
    time = db.Column(db.String(16))
    content=db.Column(db.Text(1000))
    student_id=db.Column(db.BigInteger, db.ForeignKey('tb_student.id'))
    replies = db.relationship('Reply', backref='question')


class Reply(db.Model, UserMixin):
    __tablename__ = 'tb_reply'
    id = db.Column(db.BigInteger, primary_key=True)
    time = db.Column(db.String(16))
    content = db.Column(db.Text(1000))
    person = db.Column(db.String(5))
    question_id = db.Column(db.BigInteger, db.ForeignKey('tb_question.id'))


class Sign(db.Model, UserMixin):
    __tablename__ = 'tb_sign'
    sign_time=db.Column(db.String(32),primary_key=True)
    student_id = db.Column(db.BigInteger, db.ForeignKey('tb_student.id'))
####################################################################################
#  下面是自己定义的函数


@login_manager.user_loader   # 由于学生学号是12位，教师工号是11位，顾进行回调加载用户
def load_user(user_id):
    if int(user_id) > 99999999999:
        return Student.query.get(int(user_id))
    elif int(user_id) <= 99999999999:
        return Teacher.query.get(int(user_id))


def return_user_page(user_id):               # 定义一个方法，用于判断是老师还是学生，从而返回相应的首页
    if int(user_id) > 99999999999:
        return redirect(url_for('main.index'))
    elif int(user_id) <= 99999999999:
        return redirect(url_for('main.teacher'))

# datetime 本身支持比较大小
# def compare_time(teacher_time,final_time):


def check_file(filename):  # 首先判断他的文件名正确，然后改名字，保存
    if '.' in filename and filename.rsplit('.',1)[1] in config.Config.ALLOWED_EXTENSIONS:
        ext=os.path.splitext(filename)[1]
        new_filename = uuid.uuid4().hex+ext
        return new_filename
    else:
        return None


def connect():  # 链接数据库的操作封装
    con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password=os.environ.get('ps'),
                          database='db_pw')
    cursor = con.cursor()
    return con,cursor


def connection(func):
    @functools.wraps(func)
    def inner(*args,**kwargs):  # *args表示位置参数(以(a,b,...)的形式传入的元组)，**kwargs表示关键字参数（(以a=1,b=2)形式传入的字典）
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password=os.environ.get('ps'),
                              database='db_pw')  # *args为必选参数，**kwargs为可选参数
        cursor = con.cursor()
        res = func(cursor,**kwargs)  # 先传入cursor,另外一个用**kwargs占位，等下一个装饰器传入。
        cursor.close()
        con.commit()
        con.close()
        return res
    return inner  # 开头结尾都不用自己写，只用写核心执行逻辑



def math_timel(func):  # 装饰器本质对被装饰的函数进行处理，返回增强功能后的函数
    def inner(*args):
        print('123')
        res=func(*args)
        print('456')
        return res
    return inner


# class Role(db.Model):
#     __tablename__ = 'tb_role'
#     id = db.Column(db.BigInteger, primary_key=True)
#     name = db.Column(db.String(10),unique=True)
#     default=db.Column('db.Boolean',default=False,index=True)
#     permission=db.Column(db.Integer)
#     users = db.relationship('User', backref='role',lazy='dynamic')
#
#     def __init__(self,**kwargs):
#         super(Role,self).__init__(**kwargs)
#         if self.permissions is None:
#             self.permissions=0
