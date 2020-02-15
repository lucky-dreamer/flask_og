from flask import Blueprint
auth=Blueprint('auth',__name__)
from . import views


#  将登陆相关的视图函数单独放一个文件夹，这里注册到蓝本中