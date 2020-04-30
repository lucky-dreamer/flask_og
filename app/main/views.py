from flask import render_template,session,flash,redirect,url_for,request,send_from_directory
from datetime import datetime
from .import main
from .forms import generate_introduce_Form, Inform, FileForm, GradePowerForm, SignNumberForm, StudentNumberForm, AskForm, ReplyForm
import pymysql
from ..email import send_email
from flask_login import login_required
from ..models import check_file
from flask_login import current_user
from ..models import Informs,Question,Student,Reply,Teacher,Sign
import os
from .. import db
import config
from flask_ckeditor import upload_fail,upload_success


@main.route('/')             # 这里把学生登陆首页作为网页的根页面
@login_required
def index():                           # 这里同时引入时间变量，传入现在的datetime时间给它，以便等下在模板中使用
    return render_template('pt_student.html', current_time=datetime.utcnow())


@main.route('/first_choice')  # 学生选择
def first_choice():  # 这里的查询语句比较复杂，所以用pymysql会更灵活一些
    if current_user.teacher_id is not None:   # 时间的渲染
        teacher_time=current_user.teacher.teacher_time
        final_time=current_user.teacher.final_time
    else:
        teacher_time='初选时间'
        final_time = '最终确定时间'
    contented = []     # 用于存放最终的数据
    con = pymysql.connect(host='localhost',port=3306,user='root',password=os.environ.get('ps'),database='db_pw')  # 这里后期要改
    cursor=con.cursor()
    sql1 = 'select id,name,theme,contain from tb_teacher where introduction is not NULL'
    cursor.execute(sql1)  # 从教师表中查询的数据
    content=cursor.fetchall()
    cursor.close()
    cursor = con.cursor()
    for x in content:
        p=list(x)   # 转化为列表方便增加元素
        sql2 = 'select count(tb_student.teacher_id) from ' \
               'tb_student,tb_teacher where tb_student.teacher_id=tb_teacher.id and tb_teacher.id = {}'.format(
            x[0])  # 用连接查询统计出每位教师被多少名学生选择
        cursor.execute(sql2)
        s=cursor.fetchone()[0]
        p.append(s)
        contented.append(p)   # 放入新的列表中
    try:
        sql3='select tb_teacher.name from tb_student,tb_teacher where tb_teacher.id=tb_student.teacher_id and ' \
             'tb_student.teacher_id={}'.format(current_user.teacher_id)
        # 查询目前的教师，如果还没选的话就无
        cursor.execute(sql3)
        teacher = cursor.fetchall()[0][0]
    except:
        teacher = '还未选择'
    cursor.close()
    con.close()
    return render_template('first_choice.html', contented=contented,teacher=teacher,teacher_time=teacher_time,final_time=final_time)


@main.route('/introduce<id>')
def introduces(id):
    introduction=Teacher.query.filter_by(id=id).first().introduction
    return render_template('introduce.html',introduction=introduction)


@main.route('/after_choice/<id>')
def after_choice(id):     # 学生选择完之后进行相应的操作
    con = pymysql.connect(host='localhost', port=3306, user='root', password=os.environ.get('ps'), database='db_pw')  # 这里后期要改
    cursor = con.cursor()
    sql1 = 'select count(teacher_id),tb_teacher.contain,tb_teacher.teacher_time,tb_teacher.final_time from tb_teacher,' \
           'tb_student where tb_student.teacher_id=tb_teacher.id and tb_teacher.id={}'.format(id)
    cursor.execute(sql1)
    data=cursor.fetchone()
    cursor.close()
    con.close()
    selected = data[0]  # 这里在数据库中拿出选择人数，课程容量，时间等
    contain = data[1]
    teacher_time = datetime.strptime(data[2], '%Y-%m-%d')
    final_time = datetime.strptime(data[3], '%Y-%m-%d')
    now = datetime.now()
    if now < teacher_time:    # 初选
        current_user.teacher_id = id   # 选完以后，存入相应的教师id
        current_user.personal_theme=current_user.teacher.theme
        db.session.commit()
        flash('选择成功')
    elif now > teacher_time:  # 终选
        if selected < contain:
            current_user.teacher_id = id  # 选完以后，存入相应的教师id
            current_user.personal_theme = current_user.teacher.theme
            db.session.commit()
            flash('选择成功')
        elif selected >= contain:
            flash('已经选满')
    return redirect(url_for('main.first_choice'))


@main.route('/informs')  # 公告内容
def informs():
    id=current_user.teacher_id
    inform=Informs.query.filter_by(teacher_id=id).all()
    return render_template('informs.html',inform=inform)


@main.route('/up_file',methods=['GET','POST'])
def up_file():
    form=FileForm()
    if form.validate_on_submit():
        if current_user.teacher is None:
            flash('请先选择教师')
        else:
            if current_user.file_url:
                x = current_user.file_url.split('upfile/', 1)[1]  # 数据库中存的是完整的url，这里拿到文件名
                path = os.path.join(config.Config.UPFILE_FOLDER, x)  # 再拼接成完整路径
                os.remove(path)  # 删除
                current_user.file_url='NULL'  # 同时在数据库中删除
                current_user.file_name='NULL'
                db.session.commit()
            try:
                file = form.inform.data  # 拿到文件
                old_name = file.filename
                if check_file(old_name):  # 验证以及改名字,改名字更安全，防止黑客攻击
                    filename = check_file(file.filename)
                    file.save(os.path.join(config.Config.UPFILE_FOLDER, filename))  # 保存
                    flash('上传成功')
                    session['file_url'] = url_for('main.openfile', filename=filename)
                    current_user.file_url=session.get('file_url')
                    current_user.file_name=old_name
                    db.session.commit()
                else:
                    flash('文件名格式不正确')
                return redirect(url_for('main.up_file'))
            except:
                flash('出现了未知错误')
    return render_template('up_file.html', form=form,f=current_user.file_name,a=current_user.file_url)


@main.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = StudentNumberForm()
    if current_user.teacher is not None:
        number = current_user.teacher.sign_number  # 查询现在的签到码
        if form.validate_on_submit():  # 学生提交签到码
            if form.sign_number.data == number:  # 如果正确
                if current_user.is_sign == 0:  # 并且是教师发起签到的首次提交
                    # current_user.sign_times += 1   # 学生自己的累计签到次数加一，如果一个学生签到很多次呢？？
                    current_user.is_sign += 1  # 学生签到的实时统计数据
                    gn=Sign(sign_time=datetime.now().strftime('%m-%d %H:%M:%S.%f'),
                            student_id=current_user.id)
                    db.session.add(gn)
                    db.session.commit()
                    flash('签到成功')
                else:
                    flash('你已经签到完成，请勿重复提交')
            else:
                flash('签到码错误')
    else:
        flash('你还未选择老师')
    return render_template('sign_in.html', form=form)


@main.route('/ask_question', methods=['GET', 'POST'])  # 这里后期还可以改用富文本编辑器
def ask_question():
    form = AskForm()  # 将学生提问数据存到数据库中
    if form.validate_on_submit():
        ct=Question(time=datetime.now().strftime('%m-%d %H:%M'),
                    content=form.question.data,
                    student_id=current_user.id)
        db.session.add(ct)
        db.session.commit()
        flash('成功')
    return render_template('ask_question.html', form=form)


@main.route('/questions')
def questions():  # 查看所有同组同学提过的问题以及老师的解答
    lis = []
    if current_user.teacher is not None:
        for x in current_user.teacher.students:
            for j in x.questions:
                lis.append(j)
        lis=lis[::-1]
    else:
        flash('请先选择教师')
    return render_template('questions.html',lis=lis)


@main.route('/my_question')
def my_question():   # 查看自己的提问
    question=current_user.questions
    question=question[::-1]
    return render_template('my_question.html',question=question)


@main.route('/delete_question<id>')
def delete_question(id):
    s=Question.query.get(id)
    db.session.delete(s)
    db.session.commit()
    return "<h4>删除成功</h4>"

####################################################################################


@main.route('/teacher', methods=['GET', 'POST']) # 教师首页
@login_required
def teacher():
    return render_template('pt_teacher.html', current_time=datetime.utcnow())


@main.route('/teacher/first_content')
def first_content():
    return render_template("first_content.html")


@main.route('/teacher/generate', methods=['GET', 'POST'])
@login_required    # 生成课题简介
def generate():
    form = generate_introduce_Form()
    if current_user.introduction is None:
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
    return redirect(url_for('main.generated'))


@main.route('/teacher/generated', methods=['GET', 'POST'])  # 生成后的页面
def generated():
    theme=current_user.theme     # 直接用current_user就可以方便的访问当前用户的所有属性
    introduce=current_user.introduction
    contain = current_user.contain
    teacher_time = current_user.teacher_time
    final_time = current_user.final_time
    return render_template('teacher_generated.html', theme=theme,introduce=introduce,contain=contain,teacher_time=teacher_time,final_time=final_time)


@main.route('/teacher/change', methods=['GET', 'POST'])  # 修改简介
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


@main.route('/teacher/teacher_choice')  # 教师选择
def teacher_choice():
    con = pymysql.connect(host='localhost', port=3306, user='root',
                          password=os.environ.get('ps'), database='db_pw')  # 这里后期要改
    cursor = con.cursor()
    sql1 = 'select count(teacher_id) from tb_teacher,tb_student where' \
           ' tb_student.teacher_id=tb_teacher.id and tb_teacher.id={}'.format(current_user.id)
    cursor.execute(sql1)
    selected=cursor.fetchone()[0]  # 直接用current_user.students.count()不知道为啥会报错，所以这里用pymysql
    cursor.close()
    con.close()
    contain=current_user.contain
    content=current_user.students
    teacher_time=current_user.teacher_time
    return render_template('teacher_choice.html',selected=selected,contain=contain,content=content,teacher_time=teacher_time)


# 登陆那块用orm比较多，主函数中pymysql多一点
@main.route('/teacher/deletes/<id>', methods=['GET', 'POST'])  # 进行选择的操作
def deletes(id):   # 传回学生id用于待会儿查询
    for i in current_user.students:
        if i.file_url is not None:
            x = i.file_url.split('upfile/', 1)[1]  # 数据库中存的是完整的相对url，这里拿到文件名
            path = os.path.join(config.Config.UPFILE_FOLDER, x)  # 再拼接成完整绝对路径
            os.remove(path)
    con = pymysql.connect(host='localhost', port=3306, user='root', password=os.environ.get('ps'), database='db_pw')  # 这里后期要改
    cursor = con.cursor()
    sql4 = "delete from tb_question where student_id={}".format(id)  # 删除问题表
    sql5="update tb_student set teacher_id=NULL,file_url=NULL,file_name=NULL,grade=NULL" \
         ",is_sign=0 where teacher_id={}".format(current_user.id)
    cursor.execute(sql4)
    cursor.execute(sql5)
    con.commit()   # 这里一定要记着提交更改到数据库
    cursor.close()
    con.close()
    flash('删除成功')
    return redirect(url_for('main.teacher_choice'))


@main.route('/teacher/different_theme',methods=['GET','POST'])
def different_theme():
    students = current_user.students  # 加载学生说明书
    if request.method == 'POST':  # 如果表单提交
        for i in students:  # 通过键拿到输入分数，乘以相应的权重，再相加
            p = request.form.get("{}".format(i.id))
            i.personal_theme=p
        db.session.commit()
        flash('成功')
        return redirect(url_for('main.teacher_choice'))
    return render_template('different_theme.html', students=students)


@main.route('/teacher/up_inform/',methods=['GET','POST'])
def up_inform():  # 上传公告
    form=Inform()
    if form.validate_on_submit():
        file=form.inform.data                     # 拿到文件
        old_name=file.filename
        if check_file(old_name):  # 验证以及改名字,改名字更安全，防止黑客攻击
            filename=check_file(file.filename)
            file.save(os.path.join(config.Config.UPFORM_FOLDER,filename))  # 保存
            flash('上传成功')
            session['file_url']=url_for('main.openform',filename=filename)
            inform=Informs(url=session.get('file_url'),
                           title=old_name,
                           teacher_id=current_user.id)
            db.session.add(inform)  # 添加到数据库中
            db.session.commit()
        else:
            flash('文件名格式不正确')
        return redirect(url_for('main.up_inform'))
    return render_template('up_inform.html',form=form,file_url=session.get('file_url'))



@main.route('/teacher/my_informs')
def my_informs():  # 教师查看公告内容
    id = current_user.id
    inform = Informs.query.filter_by(teacher_id=id).all()
    li={}    # 数据库中存相对路径会好一点，但是再删除公告回传的时候会出问题，所以这里进行一定的处理再传入模板，回传的是处理过的url，但是数据库中存的还是正确的url
    for x in inform:
        p='h:'+x.url
        li[x]=p
    return render_template('my_informs.html',inform=inform,li=li)


@main.route('/teacher/delete_inform/<path:url>')   # 数据类型path表明传的是路径，可以包含/
def delete_inform(url):  # 删除相应的公告
    x = url.split('uploads/',1)[1]    # 数据库中存的是url，这里拿到文件名
    path = os.path.join(config.Config.UPFORM_FOLDER, x)  # 再拼接成完整路径
    os.remove(path)  # 删除
    url = url.split(':', 1)[1]
    tr = Informs.query.filter_by(url=url).first()  # 同时在数据库中删除
    db.session.delete(tr)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('main.my_informs'))


@main.route('/teacher/generate_grades',methods=['GET','POST'])
def generate_grades():
    form1 = GradePowerForm()
    if form1.validate_on_submit():
        session['daily'] = form1.daily.data  # 教师输入成绩的权重
        session['answer'] = form1.answer.data
        session['final'] = form1.final.data
        flash('设置成功')
        return redirect(url_for('main.math_grade'))  # 进入输入各项成绩的页面
    return render_template('grades.html', form1=form1)


@main.route('/teacher/math_grade',methods=['GET','POST'])
def math_grade():
    students = current_user.students  # 加载学生说明书
    if request.method == 'POST':  # 如果表单提交
        for i in students:  # 通过键拿到输入分数，乘以相应的权重，再相加
            p = eval(request.form.get("{}".format(i.id))) * eval(session.get('daily')) + \
                eval(request.form.get("{}".format(i.name))) * eval(session.get('answer')) +\
                eval(request.form.get("{}".format(i.file_name))) * eval(session.get('final'))
            i.grade=str(p)
        db.session.commit()
        try:
            flash('成功')
            return redirect(url_for('main.grade_result'))
        except:
            flash('输入格式有误')
    return render_template('math_grade.html',students=students,daily=session.get('daily'),answer=session.get('answer'),final=session.get('final'))


@main.route('/teacher/grade_result',methods=['GET','POST'])
def grade_result():
    students=current_user.students  # 计算后的结果
    return render_template('grade_result.html',students=students)


@main.route('/teacher/sign_number',methods=['GET', 'POST'])
def sign_number():
    form = SignNumberForm()
    if form.validate_on_submit():  # 如果教师提交了签到码
        for x in current_user.students:
            x.is_sign = 0  # 这次签到，需要把上次签到的实时数据清零
        current_user.sign_number = form.sign_number.data  # 把签到码存到数据库
        db.session.commit()
        flash('生成成功')
        return redirect(url_for('main.signed'))
    return render_template('sign_number.html', form=form)


@main.route('/teacher/signed',methods=['GET','POST'])
def signed():
    students=current_user.students
    number=current_user.sign_number
    all_student = 0                    # 这里想count学生的数量
    now = 0                            # 记录实时签到的人数
    for x in students:
        all_student += 1
        if x.is_sign == 1:           # 将完成签到的学生统计
            now += 1
    return render_template('signed.html',students=students,number=number,p=now,contain=all_student)


@main.route('/teacher/history_sign<id>')
def history_sign(id):
    info=Sign.query.filter_by(student_id=id).all()
    return render_template('history_sign.html',info=info)


@main.route('/teacher/questions_for_teacher')
def questions_for_teacher():  # 教师查看自己学生的问题
    lis = []
    for x in current_user.students:
        for j in x.questions:
            lis.append(j)  # 将所有问题暂存一个列表之中
    lis=lis[::-1]
    return render_template('questions_for_teacher.html',lis=lis)


@main.route('/teacher/reply/<id>', methods=['GET', 'POST'])
def reply(id):  # 进行问题的回复，这里学生回复一样用这个视图函数
    form=ReplyForm()
    if form.validate_on_submit():
        reply=Reply(time=datetime.now().strftime('%m-%d %H:%M'),
                    content=form.reply.data,
                    question_id=id,
                    person=current_user.name)
        db.session.add(reply)
        db.session.commit()
        if current_user.id > 99999999999:  # 判断是教师还是学生，回复过后返回相应的页面
            return redirect(url_for('main.my_question'))
        elif current_user.id < 99999999999:
            return redirect(url_for('main.questions_for_teacher'))
    return render_template('reply.html',form=form)


@main.route('/teacher/is_ending')
def is_ending():
    return render_template('is_ending.html')


# 图片就不设置删除管理了，到时候1年清理一次就可以。或者正则匹配源码中的图片，再删除？？
@main.route('/teacher/ending_course')
def ending_course():
    con = pymysql.connect(host='localhost', port=3306, user='root', password=os.environ.get('ps'),
                          database='db_pw')  # 这里后期要改
    cursor = con.cursor()  # 先删文件，再删数据库
    for j in current_user.informs:
        if j.url is not None:
            y = j.url.split('upform/', 1)[1]
            paths = os.path.join(config.Config.UPFORM_FOLDER, y)
            os.remove(paths)  # 删除通知
    for i in current_user.students:
        if i.file_url is not None:
            x = i.file_url.split('upfile/', 1)[1]  # 数据库中存的是完整的相对url，这里拿到文件名
            path = os.path.join(config.Config.UPFILE_FOLDER, x)  # 再拼接成完整绝对路径
            os.remove(path)  # 删除说明书
        # for m in i.questions:
        #     sql3="delete from tb_reply where question_id={}".format(m.id)
        #     cursor.execute(sql3)
        #     con.commit()  # 删除回复表  删除问题表，回复表就会自动消失，外键约束
        # cursor.close()
        cursor=con.cursor()
        sql4="delete from tb_question where student_id={}".format(i.id)  # 删除问题表
        cursor.execute(sql4)
        con.commit()
    sql0 = "update tb_teacher set theme=NULL,introduction=NULL,contain=NULL,final_time=NULL,teacher_time=NULL" \
           ",sign_number=NULL where name='{}'".format(current_user.name)

    sql1="update tb_student set teacher_id=NULL,file_url=NULL,file_name=NULL,grade=NULL" \
         ",sign_times=0,is_sign=0 where teacher_id={}".format(current_user.id)
    sql2="delete from tb_inform where teacher_id={}".format(current_user.id)
    cursor.execute(sql0)
    cursor.execute(sql1)
    cursor.execute(sql2)
    con.commit()
    cursor.close()
    con.close()
    return '<h1>成功</h1>'


################################################################################################


# 编写视图函数，调用函数进行邮件发送
@main.route('/email', methods=['GET', 'POST'])
def send_mail():
    send_email(subject='first_mail', to=['824594979@qq.com', '2170703563@qq.com'], template='lv')
    return '<h1>发送成功</h1>'


@main.route('/upform/<filename>')
def openform(filename):        # 根据路径下载以及打开文件
    return send_from_directory(config.Config.UPFORM_FOLDER,filename=filename)


@main.route('/upfile/<filename>')
def openfile(filename):        # 根据路径下载以及打开文件
    return send_from_directory(config.Config.UPFILE_FOLDER,filename=filename)


@main.route('/open_image/<path:filename>')
def uploaded_files(filename):
    path = 'G:/flask_og/app/static/paragraph_image'
    return send_from_directory(path,filename)


@main.route('/upload',methods=['GET','POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'jpeg', 'png']:
        return upload_fail(message='只支持图片上传')
    f.save(os.path.join('G:/flask_og/app/static/paragraph_image', f.filename))
    url=url_for('main.uploaded_files',filename=f.filename,_external=True)
    return upload_success(url=url)


# print(datetime.now().strftime('%m-%d %H:%M'))
