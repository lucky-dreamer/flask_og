  # 验证用户登陆状态的模型
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
  # 数据库


class User(db.Model,UserMixin):
        __tablename__ = 'tb_user'
        id = db.Column(db.BigInteger, primary_key=True)  # 账号（写学号）
        name = db.Column(db.String(5))                    # 真实姓名
        phone = db.Column(db.String(64))
        hash_password = db.Column(db.String(128), nullable=False)  # 密码
        role_id = db.Column(db.BigInteger, db.ForeignKey('tb_role.id'))

# 在多端加入外键，在一端加入关系

        @property
        def password(self):
            raise ArithmeticError('密码是不可访问的')

        @password.setter
        def password(self, password):
            self.hash_password = generate_password_hash(password)

        def verify_password(self, password):
            return check_password_hash(self.hash_password, password)


class Role(db.Model):
    __tablename__ = 'tb_role'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(10))
    users = db.relationship('User', backref='role')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
