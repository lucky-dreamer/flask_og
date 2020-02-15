from threading import Thread
from flask_mail import Message
from flask import render_template,current_app
from . import mail


def send_async_email(app,msg):       # 这里必须调用上下文app_context来共享
    with app.app_context():
        mail.send(msg)


def send_email(subject, to, template, **kwargs):  # 定义邮件标题，接收者，邮件主体，主体放入模板中渲染
    app=current_app._get_current_object()          # 调用current_app,传入现在的app对象
    msg=Message(subject, recipients=to)
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    asyn=Thread(target=send_async_email, args=[app, msg])   # 调用多线程
    asyn.start()


# # 编写视图函数，调用函数进行邮件发送
# @app.route('/email', methods=['GET', 'POST'])
# def send_mail():
#     send_email(subject='first_mail', to=['824594979@qq.com', '2170703563@qq.com'], template='lv')
#     return '<h1>发送成功</h1>'


