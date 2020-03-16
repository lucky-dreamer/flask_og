  # 验证用户登陆状态的模型
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask import redirect,url_for
import time
from datetime import datetime
  # 数据库


class Student(db.Model, UserMixin):
        __tablename__ = 'tb_student'
        id = db.Column(db.BigInteger, primary_key=True)  # 账号（写学号）
        name = db.Column(db.String(5))                    # 真实姓名
        phone = db.Column(db.String(64))
        hash_password = db.Column(db.String(128), nullable=False)  # 密码
        teacher_id = db.Column(db.BigInteger, db.ForeignKey('tb_teacher.id'))


# 在多端加入外键，在一端加入关系

        @property
        def password(self):
            raise ArithmeticError('密码是不可访问的')

        @password.setter
        def password(self, password):
            self.hash_password = generate_password_hash(password)

        def verify_password(self, password):
            return check_password_hash(self.hash_password, password)



class Teacher(db.Model, UserMixin):
    __tablename__ = 'tb_teacher'
    id = db.Column(db.BigInteger, primary_key=True)  # 账号（写学号）
    name = db.Column(db.String(5))  # 真实姓名
    phone = db.Column(db.String(64))
    hash_password = db.Column(db.String(128), nullable=False)  # 密码
    theme = db.Column(db.String(64),nullable=True)
    introduction = db.Column(db.Text(1000),nullable=True)
    contain = db.Column(db.Integer)
    students = db.relationship('Student', backref='teacher')  # 学生的老师，老师的学生们直接用关系来访问
    teacher_time = db.Column(db.String(16))
    final_time = db.Column(db.String(16))
    # role_id = db.Column(db.BigInteger, db.ForeignKey('tb_role.id'))

    # 在多端加入外键，在一端加入关系

    @property
    def password(self):
        raise ArithmeticError('密码是不可访问的')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)


####################################################################################
#  下面是自己定义的函数



@login_manager.user_loader   # 由于学生学号是12位，教师工号是11位，顾进行回调加载用户
def load_user(user_id):
    if int(user_id)>99999999999:
        return Student.query.get(int(user_id))
    elif int(user_id)<999999999999:
        return Teacher.query.get(int(user_id))


def return_user_page(user_id):               # 定义一个方法，用于判断是老师还是学生，从而返回相应的首页
    if int(user_id)>99999999999:
        return redirect(url_for('main.index'))
    elif int(user_id)<999999999999:
        return redirect(url_for('main.teacher'))

# datetime 本身支持比较大小
# def compare_time(teacher_time,final_time):












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
