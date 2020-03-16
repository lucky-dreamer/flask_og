from flask import render_template,session,flash,redirect,url_for
from datetime import datetime
from .import main
from .forms import generate_introduce_Form
import pymysql
from ..email import send_email
from flask_login import login_required
from ..models import Student,Teacher
from flask_login import current_user
from .. import db
import os


@main.route('/')             # 这里把学生登陆首页作为网页的根页面
@login_required
def index():                           # 这里同时引入时间变量，传入现在的datetime时间给它，以便等下在模板中使用
    return render_template('pt_student.html', current_time=datetime.utcnow())


@main.route('/first_choice')
def first_choice():  # 这里的查询语句比较复杂，所以用pymysql会更灵活一些
    if current_user.teacher_id is not None:
        teacher_time=current_user.teacher.teacher_time
        final_time=current_user.teacher.final_time
    else:
        teacher_time='teacher_time'
        final_time = 'final_time'
    contented = []     # 用于存放最终的数据
    db = pymysql.connect(host='localhost',port=3306,user='root',password=os.environ.get('ps'),database='db_pw')  # 这里后期要改
    cursor=db.cursor()
    sql1 = 'select id,name,theme,introduction,contain from tb_teacher where introduction is not NULL'
    cursor.execute(sql1)  # 从教师表中查询的数据
    content=cursor.fetchall()
    cursor.close()
    cursor = db.cursor()
    for x in content:
        p=list(x)   # 转化为列表方便增加元素
        sql2 = 'select count(tb_student.teacher_id) from tb_student,tb_teacher where tb_student.teacher_id=tb_teacher.id and tb_teacher.id = {}'.format(
            x[0])  # 用连接查询统计出每位教师被多少名学生选择
        cursor.execute(sql2)
        s=cursor.fetchone()[0]
        p.append(s)
        contented.append(p)   # 放入新的列表中
    try:
        sql3='select tb_teacher.name from tb_student,tb_teacher where tb_teacher.id=tb_student.teacher_id and tb_student.teacher_id={}'.format(current_user.teacher_id)
        # 查询目前的教师，如果还没选的话就无
        cursor.execute(sql3)
        teacher = cursor.fetchall()[0][0]
    except:
        teacher = '还未选择'
    cursor.close()
    db.close()
    return render_template('first_choice.html', contented=contented,teacher=teacher,teacher_time=teacher_time,final_time=final_time)


@main.route('/after_choice/<id>')
def after_choice(id):
    con = pymysql.connect(host='localhost', port=3306, user='root', password=os.environ.get('ps'), database='db_pw')  # 这里后期要改
    cursor = con.cursor()
    sql1 = 'select count(teacher_id),tb_teacher.contain,tb_teacher.teacher_time,tb_teacher.final_time from tb_teacher,tb_student where tb_student.teacher_id=tb_teacher.id and tb_teacher.id={}'.format(id)
    cursor.execute(sql1)
    data=cursor.fetchone()
    cursor.close()
    con.close()
    selected = data[0]  # 这里在数据库中拿出选择人数，课程容量，时间等
    contain = data[1]
    teacher_time = datetime.strptime(data[2],'%Y-%m-%d')
    final_time = datetime.strptime(data[3],'%Y-%m-%d')
    now = datetime.now()
    if now<teacher_time:
        current_user.teacher_id = id   # 选完以后，存入相应的教师id
        db.session.add(current_user)
        db.session.commit()
        flash('选择成功')
    elif now>teacher_time:
        if selected<contain:
            current_user.teacher_id = id  # 选完以后，存入相应的教师id
            db.session.add(current_user)
            db.session.commit()
            flash('选择成功')
        elif selected>=contain:
            flash('已经选满')
    return redirect(url_for('main.first_choice'))

####################################################################################


@main.route('/teacher', methods=['GET', 'POST'])
@login_required
def teacher():
    return render_template('pt_teacher.html', current_time=datetime.utcnow())


@main.route('/teacher/generate', methods=['GET', 'POST'])
@login_required
def generate():
    form = generate_introduce_Form()
    if current_user.introduction is None:
        if form.validate_on_submit():
            flash('你已经成功生成课程简介')
            current_user.theme = form.theme.data
            current_user.introduction = form.introduce.data
            current_user.contain = form.contain.data
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('main.generated'))
        return render_template('teacher_generate.html', form=form)
    return redirect(url_for('main.generated'))


@main.route('/teacher/generated', methods=['GET', 'POST'])
def generated():
    theme=current_user.theme     # 直接用current_user就可以方便的访问当前用户的所有属性
    introduce=current_user.introduction
    contain = current_user.contain
    teacher_time = current_user.teacher_time
    final_time = current_user.final_time
    return render_template('teacher_generated.html', theme=theme,introduce=introduce,contain=contain,teacher_time=teacher_time,final_time=final_time)


@main.route('/teacher/change', methods=['GET', 'POST'])
def change():                # 比生成少一个判断
    form = generate_introduce_Form()
    if form.validate_on_submit():
        flash('你已经成功生成课程简介')
        current_user.theme = form.theme.data
        current_user.introduction = form.introduce.data
        current_user.contain = form.contain.data
        current_user.teacher_time = form.teacher_time.data
        current_user.final_time = form.final_time.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('main.generated'))
    return render_template('teacher_generate.html', form=form)


@main.route('/teacher/teacher_choice')
def teacher_choice():
    db = pymysql.connect(host='localhost', port=3306, user='root', password=os.environ.get('ps'), database='db_pw')  # 这里后期要改
    cursor = db.cursor()
    sql1 = 'select count(teacher_id) from tb_teacher,tb_student where tb_student.teacher_id=tb_teacher.id and tb_teacher.id={}'.format(current_user.id)
    cursor.execute(sql1)
    selected=cursor.fetchone()[0]  # 直接用current_user.students.count()不知道为啥会报错，所以这里用pymysql
    cursor.close()
    db.close()
    contain=current_user.contain
    content=current_user.students
    teacher_time=current_user.teacher_time
    return render_template('teacher_choice.html',selected=selected,contain=contain,content=content,teacher_time=teacher_time)


# 登陆那块用orm比较多，主函数中pymysql多一点
@main.route('/teacher/deletes/<id>', methods=['GET', 'POST'])
def deletes(id):   # 传回学生id用于待会儿查询
    db = pymysql.connect(host='localhost', port=3306, user='root', password=os.environ.get('ps'), database='db_pw')  # 这里后期要改
    cursor = db.cursor()
    sql0='set FOREIGN_KEY_CHECKS=0'
    sql1 = 'update tb_student set teacher_id=NULL where id={}'.format(int(id))
    sql2 = 'set FOREIGN_KEY_CHECKS=1'
    cursor.execute(sql0)
    cursor.execute(sql1)
    cursor.execute(sql2)
    db.commit()   # 这里一定要记着提交更改到数据库
    cursor.close()
    db.close()
    flash('删除成功')
    return redirect(url_for('main.teacher_choice'))









# 编写视图函数，调用函数进行邮件发送
@main.route('/email', methods=['GET', 'POST'])
def send_mail():
    send_email(subject='first_mail', to=['824594979@qq.com', '2170703563@qq.com'], template='lv')
    return '<h1>发送成功</h1>'
