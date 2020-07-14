from flask import render_template,redirect,request,url_for,flash,globals  # 登陆的功能单独开一个蓝本模块
from .import auth
from flask_login import login_user,login_required,logout_user,current_user
from ..models import Student,Teacher,return_user_page
from .forms import LoginForm,ChangeFile_Form,Forget_Form,Check_Code_f
from flask import session
from .forms import RegisterForm,Check_Code
from .. import db
from .message import check_number
import random


@auth.route('/login',methods=['GET','POST'])              # 登陆页面
def login():
    form=LoginForm()
    if form.validate_on_submit():# 如果提交表单
        if form.role.data==1:
            student=Student.query.filter_by(id=form.id.data).first()    # 查找id所对应的对象
            if student is not None and student.verify_password(form.old_pw.data):
                login_user(student, form.remember_me.data)
                next = request.args.get(
                    'next')  # 引用next 参数来辅助判断，查询字符串保存到当中，如果是原来字符串，则说明数据库中没有该角色，不能登陆，如果变了，则访问了首页，能标记登陆
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
            flash('不合法的用户名或密码')
        elif form.role.data==2:
            teacher = Teacher.query.filter_by(id=form.id.data).first()
            if teacher is not None and teacher.verify_password(form.old_pw.data): # 如果对象存在且密码正确
                login_user(teacher,form.remember_me.data)        # 把用户标记为以登陆，同时是否记住，从这里开始就可以用current_user来操作
                next=request.args.get('next')        # 引用next 参数来辅助判断，查询字符串保存到当中，如果是原来字符串，则说明数据库中没有该角色，不能登陆，如果变了，则访问了首页，能标记登陆
                if next is None or not next.startswith('/'):
                    next=url_for('main.index')
                return redirect(next)  # 只能有一个首页（根路由），否则会因为”next“参数而产生错误，具体的页面返回在这个根路由里面处理
            flash('不合法的用户名或密码')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登录')
    return redirect(url_for('auth.login'))


@auth.route("/register",methods=['GET','POST'])
def register():
    form=RegisterForm()                 # 由于要用手机号发验证码，所以这里要分两次提交两个表单
    form2=Check_Code()
    if form2.validate_on_submit():       # 点击发送验证码
        session['code'] = random.randint(1000, 9999)     # 随机生成一个4位数保存到会话中以便等下访问
        session['phone'] = form2.phone.data              # 拿到用户输入的手机号
        p = check_number(session.get('code'), session.get('phone'))  # 传入接口中进行验证码发送
        flash(p)                                           # 闪现发送状态
    elif form.validate_on_submit():                       # 用户拿到验证码后，进行信息的填写并提交
        code2=form.code.data                              # 拿到用户输入的验证码，与生成的验证码做对比
        if code2==session.get('code'):              # 如果验证码正确则向数据库中插入数据
            if form.role.data==1:
                globals.g.user = Student(id=form.id.data,
                                         name=form.name.data,
                                         password=form.cf_pw.data,
                                         phone=session.get('phone'))
                                       # role_id=1)
            elif form.role.data==2:
                globals.g.user = Teacher(id=form.id.data,
                                         name=form.name.data,
                                         password=form.cf_pw.data,
                                         phone=session.get('phone'))

            try:
                db.session.add(globals.g.user)         # 添加到数据库中
                db.session.commit()           # 提交
                flash('注册成功，现在可以登陆')
            except:
                db.session.rollback()        # 如果插入中途出现了错误，则回滚撤回
                flash("发生了未知错误")
            return redirect(url_for('auth.login'))   # 注册完后重定向到登陆页面
        else:
            flash('验证码有误')                     # 如果验证码不正确，则反馈给用户
    return render_template('auth/register.html',form=form,form2=form2)  # 返回注册页面
# 这里两个返回不会冲突，只能有一个返回页面

# @auth.route('/message')   # 最初的想法，想通过嵌套框架实现，障碍是需要得到用户的手机号，再发送验证码，必须两次表单提交
# def message():
#     globals.g.code = random.randint(0,9999)
#     p=check_number(globals.g.code,'15648106113')
#     return '<p>{}</p>'.format(p)


@auth.route('/Change_File', methods=['POST', 'GET'])
@login_required
def Change_File():                                       # 改密码提交的相关表单
    form = ChangeFile_Form()
    if form.validate_on_submit():               # 利用ccurrent_user 可以很方便的管理各种属性
        if current_user.verify_password(form.old_pw.data):
            current_user.password=form.cf_pw.data
            current_user.phone=form.phone.data
            db.session.add(current_user)
            db.session.commit()
            flash('你已经成功修改了基本信息')         # 闪现消息
            return return_user_page(current_user.id)          # 这里是main。pw
        else:
            flash('输入的密码有误')
    return render_template('auth/change_pw.html', form=form)


@auth.route('/forget_password',methods=['GET','POST'])
def forget_password():         # 忘记密码可以凭借学号，通过查询相应的手机号并发送验证码来修改，和注册类似
    form = Forget_Form()
    form2 = Check_Code_f()
    if form2.validate_on_submit():
        session['code'] = random.randint(1000, 9999)
        session['id'] = form2.id.data
        session['role']=form2.role.data
        if session.get('role')==1:
            user = Student.query.filter_by(id=session.get('id')).first()
            if user is not None:
                phone=user.phone
                p = check_number(session.get('code'), phone)
                flash(p)
            else:
                flash('您输入的账号有误')
        elif session.get('role')==2:
            user=Teacher.query.filter_by(id=session.get('id')).first()
            if user is not None:
                phone=user.phone
                p = check_number(str(session.get('code')), phone)
                flash(p)
            else:
                flash('您输入的账号有误')
    elif form.validate_on_submit():    # 改的操作，先获取对象，再进行相应属性的改变，然后提交
        code2 = form.code.data
        if code2 == session.get('code'):
            if session.get('role')==1:
                user = Student.query.filter_by(id=session.get('id')).first()
                user.name=form.name.data
                user.password=form.cf_pw.data
            elif session.get('role')==2:
                user = Teacher.query.filter_by(id=session.get('id')).first()
                user.name = form.name.data
                user.password = form.cf_pw.data

            try:
                db.session.commit()
                flash('密码重置成功')
            except:
                db.session.rollback()
                flash("发生了未知错误")
            return redirect(url_for('auth.login'))
        else:
            flash('验证码有误')
    return render_template('auth/forget_pw.html', form=form, form2=form2)
