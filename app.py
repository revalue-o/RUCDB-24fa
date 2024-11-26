# from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import secrets
import markdown
import os
import time
import DatabaseManager
import requests # llm

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = secrets.token_hex(16)

myDB = DatabaseManager.DatabaseManager()
myDB.connect()
#登录部分，负责人杜海乐
@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        account_type=request.form.get('account-type')
        login_success=-1
        if account_type=='teacher':
            login_success=myDB.teacher_login_check(username,password)
        else:
            login_success=myDB.student_login_check(username,password)
        

        # 简单的验证逻辑
        # if (username == 'admin' or username == 'student') and password == 'password':
        #     session['username'] = username
        # if myDB.student_login_check(username,password):
        if login_success==0:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password!'
            return render_template('login.html', error=error)

    return render_template('login.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():   # 登录部分先用的demo， 完整的在上面
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         # 简单的验证逻辑
#         if (username == 'admin' or username == 'student') and password == 'password':
#             session['username'] = username
#             return redirect(url_for('home'))
#     return render_template('login.html')

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
#是谁来创建教学班、添加课程这些？是教师还是管理员？
#先认为是管理员
'''
所有我对GUI操作的都放在这里，不要删除
目前暂定在home页面只能通过课程名进入新页面再访问作业什么的，不能通过点击home页面的“作业”进入新页面

原本的obe的首页仅仅是一个最近信息的作用，不会显示所有的作业等信息。我们暂时不实现这个功能，而是先实现obe左上角下拉菜单
进入课程的功能。
类似进入https://unicourse.ruc.edu.cn/index/homework/index/cno/2023l7fcquowtxje.html

'''
#教师添加作业、课件
@app.route('/add_work', methods=['GET', 'POST'])

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
'''
    'src', 'work'必选其一  (暂时的, 公告啥的看看还做不做)
    'date'key 在这里可以不需要, 但是需要按此排序
'''

work_outline = [
    {'name': 'Lab4. cachelab', 'type': '实验', 'status': 'timeout', 'deadline': '2024-11-26 23:59:59', 'publish_time': '2024-11-19 20:54:30', 'description': 'your description', 'requirements': 'your requirements', 'attachment_url': 'your attachment_url'},
    {'name': 'Lab4. cachelab', 'type': '实验', 'status': 'not-submitted', 'deadline': '2024-11-26 23:59:59', 'publish_time': '2024-11-19 20:54:30', 'description': 'your description', 'requirements': 'your requirements', 'attachment_url': 'your attachment_url'},
    {'name': '代码优化', 'type': '普通作业', 'status': 'not-submitted', 'deadline': '2024-11-26 23:59:59', 'publish_time': '2024-11-19 20:54:30', 'description': 'your description', 'requirements': 'your requirements', 'attachment_url': 'your attachment_url'},
    {'name': '磁盘访问', 'type': '小测验', 'status': 'submitted', 'deadline': '2024-11-26 23:59:59', 'publish_time': '2024-11-19 20:54:30', 'description': 'your description', 'requirements': 'your requirements', 'attachment_url': 'your attachment_url'},
    {'name': '磁盘访问', 'type': '小测验', 'status': 'not-submitted', 'deadline': '2024-11-26 23:59:59', 'publish_time': '2024-11-19 20:54:30', 'description': 'your description', 'requirements': 'your requirements', 'attachment_url': 'your attachment_url'},
]
'''
    work_outline keys:
        name: str  作业名
        type: str  作业类型
        status: str  作业状态  only('timeout', 'not-submitted', 'submitted')
        deadline:   截止日期 strftime('%Y-%m-%d %H:%M:%S')
        publish_time:   发布时间 strftime('%Y-%m-%d %H:%M:%S')
        description: str  作业描述
        requirements: str  作业要求  (这俩需要当成一个key吗)
        attachment_url: str  附件url
'''

files = [
    {'src': f'data/ppt{i}.pptx', 'date': '2024-11-19 22:44:46'} for i in range(15)
]
# 暂时的想法是： 在static下创建若干文件夹, src的路径只存放static/  后面的路径
# eg. static/DBMS_cjc/src/第六章.ppt  ->  src = DBMS_cjc/第六章.ppt  （src类）
#     static/DBMS_cjc/work_name/attachment.zip -> DBMS_cjc/work_name/attachment.zip
for file in files:
    file['name'] = os.path.basename(file['src'])


@app.route('/index')
def index():
    return render_template('index.html')

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

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    #TODO
    '''
    task: 从数据库读取内容到courses,upload, 下面的tasks同理
        known: username
        need: 所有courses: list
              所有upload: dict  (参考上面的courses,upload实例)
    '''
    username = session['username']

    return render_template('home.html', courses=courses, items=items, upload=upload)

@app.route('/course/<string:course_name>')
def course(course_name):
    if 'username' not in session:
        return redirect(url_for('index'))
    #TODO
    '''
        known: username, course_name
        need: 所有courses: list
    '''
    username = session['username']

    return render_template('course_main.html', courses=courses, course_name=course_name)

@app.route('/Cwork/<string:course_name>')
def Cwork(course_name):
    if 'username' not in session:
        return redirect(url_for('index'))
    #TODO
    '''
        known: username, course_name
        need: 所有courses: list
              该课程下的所有work_outline: dict  
    '''
    username = session['username']

    return render_template('course_work.html', courses=courses, work_outline=work_outline, course_name=course_name)

@app.route('/Csrc/<string:course_name>')
def Csrc(course_name):
    if 'username' not in session:
        return redirect(url_for('index'))
    #TODO
    '''
        known: username, course_name
        need: 所有courses: list
              该课程下的所有files: dict  
    '''
    username = session['username']

    return render_template('course_src.html', courses=courses, files=files, course_name=course_name)

@app.route('/chatBOT', methods=['POST'])
def chatBOT():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    msg = data.get('message', '')
    username = session['username']
    #TODO
    '''
        known: username, msg
        need: llm_response (关键是要有message项)
    '''
    llm_url = "http://10.77.40.36:9080/predict"
    llm_headers = {
        "Authorization": "4f484d4324b66bdbb835415c454fab772a14d126555d5a0df897b4a22c38706b",
        "Content-Type": "application/json",
    }
    input_data = {"input_data": msg} 
    
    response = requests.post(llm_url, headers=llm_headers, json=input_data)
    # print(response.status_code)  DEBUG 连接状态
    re_dict = response.json()  # dict item

    


    response = {
        'status': 'success',
        'message': f'收到消息: {re_dict['response']}',  # demo
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'username': username
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
