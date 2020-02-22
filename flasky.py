import os
from app import create_app,db
from app.models import Student,Teacher
from flask_migrate import Migrate
app=create_app('default')                  # 将数据库迁移和工厂函数注册到主脚本中
migrate=Migrate(app,db)

@app.shell_context_processor                  # 注册一个shell，方便进行交互式操作
def make_shell_context():
    return dict(db=db,Student=Student,Teacher=Teacher)