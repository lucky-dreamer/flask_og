from flask import render_template,session,flash,redirect,url_for
from datetime import datetime
from .import main
import pymysql
from ..email import send_email
from flask_login import login_required

@main.route('/')             # 这里把学生登陆首页作为网页的根页面
@login_required
def index():                           # 这里同时引入时间变量，传入现在的datetime时间给它，以便等下在模板中使用
    return render_template('pt_bootstrap.html', current_time=datetime.utcnow())



@main.route('/teacher')
@login_required
def teacher():
    return render_template('pt_bootstrap.html', current_time=datetime.utcnow())

# @main.route('/<name>')
# def user(name):          # user页面
#     return render_template('user.html', name=name)





# 编写视图函数，调用函数进行邮件发送
@main.route('/email', methods=['GET', 'POST'])
def send_mail():
    send_email(subject='first_mail', to=['824594979@qq.com', '2170703563@qq.com'], template='lv')
    return '<h1>发送成功</h1>'
