# from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import markdown
import os
import time
import DatabaseManager
os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = secrets.token_hex(16)
myDB=DatabaseManager.DatabaseManager()
myDB.connect()
#登录部分，负责人杜海乐
@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        account_type=request.form.get('account-type')

        # 简单的验证逻辑
        # if (username == 'admin' or username == 'student') and password == 'password':
        #     session['username'] = username
        if account_type=='teacher':
            return_val=myDB.teacher_login_check(username,password)
        else:
            return_val=myDB.student_login_check(username,password)
        print(return_val)
        if return_val==0:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'wrong username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

# @app.route('/welcome')
# def welcome():
#     username = request.args.get('username', 'Guest')
#     return f"<h1>Welcome, {username}!</h1>"
#登录部分结束
#注册部分
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        account_type=request.form.get('account-type')

        if password != password2:
            error = 'Passwords do not match!'
            return render_template('register.html', error=error)

        # 简单的验证逻辑
        if len(username) < 3 or len(password) < 6:
            error = 'Username or password is too short!'
            return render_template('register.html', error=error)

        # 注册成功
        #学工号长度必须为10，密码长度不限，学生姓名长度不超过16
        if account_type=='teacher':
            return_val=myDB.add_teacher(username,password,username)
        else:
            return_val=myDB.add_student(username,password,username)
        print("account_type: ",account_type," return val: ",return_val)
        if return_val==0:
            return redirect(url_for('login'))
        elif return_val==1:
            error = '学工号格式不符合要求'
            return render_template('register.html', error=error)
        elif return_val==2:
            error = '学生姓名不符合要求'
            return render_template('register.html', error=error)
        elif return_val==3:
            error = '用户已存在'
            return render_template('register.html', error=error)
        

    return render_template('register.html')
#注册部分结束

# TODO dhl将下面的这些列表改为从数据库中读取
# 
def get_course_list():
    return myDB.get_course_list()
## sq
courses = [
    'ICS',
    '计算机网络',
    '人工智能引论',
    '数据科学导论',
    '操作系统',
    '计算机网络',
    'DBMS',
    'ICS2',
    '马克思主义',
    '毛概',
    '程序设计',
    'photoshop',
    '数学分析'
]

items = [f"item{i}" for i in range(12)]

upload = [
    {'name': 'cjc', 'course': 'DBMS', 'src': '第六章.ppt'},
    {'name': 'cjc', 'course': 'DBMS', 'work': '实验五'},
]

work_outline = [
    {'name': 'Lab4. cachelab', 'type': '实验', 'status': 'timeout'},
    {'name': 'Lab4. cachelab', 'type': '实验', 'status': 'not-submitted'},
    {'name': '代码优化', 'type': '普通作业', 'status': 'not-submitted'},
    {'name': '磁盘访问', 'type': '小测验', 'status': 'submitted'},
    {'name': '磁盘访问', 'type': '小测验', 'status': 'not-submitted'},
]

files = [
    {'src': f'data/ppt{i}.pptx', 'date': '2024-11-19 22:44:46'} for i in range(15)
]
# 暂时的想法是： 在static下创建若干文件夹, src的路径只存放static/  后面的路径
# eg. static/DBMS_cjc/第六章.ppt  ->  src = DBMS_cjc/第六章.ppt
for file in files:
    file['name'] = os.path.basename(file['src'])


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    # print(f"home current_username: {session['username']}")
    return render_template('home.html', courses=courses, items=items, upload=upload)

@app.route('/course/<string:course_name>')
def course(course_name):
    if 'username' not in session:
        return redirect(url_for('index'))
    # print(f"course current_username: {session['username']}")
    return render_template('course_main.html', courses=courses, course_name=course_name)

@app.route('/Cwork/<string:course_name>')
def Cwork(course_name):
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('course_work.html', courses=courses, work_outline=work_outline, course_name=course_name)

@app.route('/Csrc/<string:course_name>')
def Csrc(course_name):
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('course_src.html', courses=courses, files=files, course_name=course_name)

@app.route('/privacy')
def privacy():
    with open('templates/privacy.md', 'r', encoding='utf-8') as f:
        content = f.read()
        html = markdown.markdown(content)
    return render_template('_markdown.html', content=html)

@app.route('/terms')
def terms():
    with open('templates/terms.md', 'r', encoding='utf-8') as f:
        content = f.read()
        html = markdown.markdown(content)
    return render_template('_markdown.html', content=html)




if __name__ == '__main__':
    app.run(debug=True, port=5000)