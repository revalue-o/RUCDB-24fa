# from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import secrets
import markdown
import os
import time
import DatabaseManager
import requests # llm
from datetime import datetime

os.chdir(os.path.dirname(__file__))

UPLOAD_FOLDER = 'load'

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
        # if (username == 'amin' or username == 'student') and password == 'password':
        #     session['username'] = username
        # if myDB.student_login_check(username,password):
        if login_success==0:
            session['username'] = username
            session['role'] = account_type  # 存储角色类型
            return redirect(url_for('home'))
        else:
            error = 'Invalidusername or password!'
            return render_template('login.html', error=error)

    return render_template('login.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():   # 登录部分先用的demo， 完整的在上面
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         account_type=request.form.get('account-type')

#         # 简单的验证逻辑
#         if (username == 'amin' or username == 'student') and password == 'password':
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

'''
所有我对GUI操作的都放在这里，不要删除
目前暂定在home页面只能通过课程名进入新页面再访问作业什么的，不能通过点击home页面的“作业”进入新页面

原本的obe的首页仅仅是一个最近信息的作用，不会显示所有的作业等信息。我们暂时不实现这个功能，而是先实现obe左上角下拉菜单
进入课程的功能。
类似进入https://unicourse.ruc.edu.cn/index/homework/index/cno/2023l7fcquowtxje.html

由教师添加课程什么的

'''
#courses = {}# 这一行是临时的，当从数据库中读取课程的API完成后将采用对应的API
#教师添加课程
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    """添加课程页面"""
        # 检查用户是否登录并且角色是 teacher
    if 'role' not in session or session['role'] != 'teacher':
        return "Access denied: Only teachers can add courses!", 403
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        course_description = request.form.get('course_description')
        # if course_name and course_description:
        #     # 存储课程信息
        #     courses[course_name] = {'description': course_description}
        result=myDB.add_course(course_name)
        if result==0:
            #courses[course_name] = {'description': 'fixed test str'}# 这一行是临时的，当从数据库中读取课程的API完成后将采用对应的API
            return redirect(url_for('course_page', course_name=course_name))
        elif result==1:
            return "错误的课程名称", 400
        return "课程名称和描述不能为空", 400
    return render_template('add_course.html')

@app.route('/cno/<course_name>')
def course_page(course_name):
    """课程页面"""
    # course = courses.get(course_name)
    course=course_name
    if course:
        return render_template('course.html', course_name=course_name, description='test fixed description')
    return "课程未找到", 404
@app.route('/logout')
def logout():
    session.clear()  # 清除 session 数据
    return redirect(url_for('login'))

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
    'DBMS',
    'ICS2',
    '马克思主义',
    '毛概',
    '程序设计',
    'photoshop',
    '数学分析',
    '线性代数'
]

items = [f"item{i}" for i in range(12)]

upload = [
    {'name': 'cjc', 'course': 'DBMS', 'src': '第六章.ppt'}, # 这里只需要最后的文件名
    {'name': 'cjc', 'course': 'DBMS', 'work': '实验五'},
]
'''
    'src', 'work'必选其一  (暂时的, 公告啥的看看还做不做)
    'date'key 在这里可以不需要, 但是需要按此排序
'''

work_outline = [
    {'name': 'Lab4. cachelab', 'type': '实验', 'status': 'timeout', 'deadline': '2024-11-26 23:59:59', 'publish_time': '2024-11-19 20:54:30', 'description': 'your description', 'attachment_url': 'your attachment_url'},
    {'name': 'Lab4. cachelab', 'type': '实验', 'status': 'not-submitted', 'deadline': '2024-11-26 23:59:59', 'publish_time': '2024-11-19 20:54:30', 'description': 'your description', 'attachment_url': 'your attachment_url'},
    {'name': '代码优化', 'type': '普通作业', 'status': 'not-submitted', 'deadline': '2024-11-26 23:59:59', 'publish_time': '2024-11-19 20:54:30', 'description': 'your description', 'attachment_url': 'your attachment_url'},
    {'name': '磁盘访问', 'type': '小测验', 'status': 'submitted', 'deadline': '2024-11-26 23:59:59', 'publish_time': '2024-11-19 20:54:30', 'description': 'your description', 'attachment_url': 'your attachment_url'},
    {'name': '磁盘访问', 'type': '小测验', 'status': 'not-submitted', 'deadline': '2024-11-26 23:59:59', 'publish_time': '2024-11-19 20:54:30', 'description': 'your description', 'attachment_url': 'your attachment_url'},
]
'''
    work_outline keys:
        name: str  作业名(标题)
        type: str  作业类型
        status: str  作业状态  only('timeout', 'not-submitted', 'submitted')
        deadline:   截止日期 strftime('%Y-%m-%d %H:%M:%S')
        publish_time:   发布时间 strftime('%Y-%m-%d %H:%M:%S')
        description: str  作业描述
        attachment_url: str  附件url
'''

files = [
    {'src': f'data/ppt{i}.pptx', 'date': '2024-11-19 22:44:46'} for i in range(15)
]
# 暂时的想法是： 在static下创建若干文件夹, src的路径只存放load/  后面的路径
# eg. load/DBMS_cjc/src/第六章.ppt  ->  src = DBMS_cjc/第六章.ppt  （src类）
#     load/DBMS_cjc/work_name/attachment.zip -> DBMS_cjc/work_name/attachment.zip
# name key取src的文件名
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
@app.route('/home/<course_name>')
def home(course_name=None):
    if 'username' not in session:
        return redirect(url_for('index'))
    
    username = session['username']
    role = session['role']

    # TODO
    # 找出该用户所有的upload

    switch_type = request.args.get('switch_type', None)
    filtered_upload = upload.copy()

    if course_name:
        filtered_upload = [item for item in filtered_upload if item['course'] == course_name]
    if switch_type:
        if switch_type == 'work':
            filtered_upload = [item for item in filtered_upload if 'work' in item]
        elif switch_type == 'src':
            filtered_upload = [item for item in filtered_upload if 'src' in item]

    if role == 'teacher':
        return render_template('home_teacher.html', 
                            courses=courses, 
                            items=items, 
                            upload=upload,  # 接口还没改 
                            course_name=course_name,
                            switch_type=switch_type)
    else:
        return render_template('home.html', 
                            courses=courses, 
                            items=items, 
                            upload=upload, 
                            course_name=course_name,
                            switch_type=switch_type)

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
    role = session['role']

    min_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
    if role == 'teacher':
        return render_template('course_main_publish.html', courses=courses, course_name=course_name, min_date=min_date)
    else:
        return render_template('course_main.html', courses=courses, course_name=course_name)
    
@app.route('/Cnotice/<string:course_name>')  # 新增公告栏，做不做再说
def Cnotice(course_name):
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
        'message': f'{re_dict["response"]}',  # demo
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'username': username
    }
    return jsonify(response)

@app.route('/courses_square')
def courses_square():
    return render_template('courses_square.html', courses=courses)


@app.route('/upload_file/<course_name>/src', methods=['POST'])
def upload_file(course_name):
    if 'username' not in session or session['role'] != 'teacher':
        return jsonify({
            'status': 'error',
            'message': '权限不足'
        }), 403

    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': '没有文件被上传'
        }), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': '没有选择文件'
        }), 400

    course_folder = os.path.join(
        app.config['UPLOAD_FOLDER'], 
        f"{course_name}", 
        'src'
    )
    os.makedirs(course_folder, exist_ok=True)
    file_path = os.path.join(course_folder, file.filename)
    file.save(file_path)
    file_path = os.path.relpath(file_path, app.config['UPLOAD_FOLDER'])

    # TODO
    # parameters: course_name, file_path
    # 上面的file_path例子： load/ICS/src/env.yml 存进数据库是只需要存 ICS/src/env.yml
    # 这里还没有考虑ICS课多个老师开的情况, 课程名+老师名能不能做key, 如ICS_柴云鹏/src/env.yml
    
    return jsonify({
        'status': 'success',
        'message': '文件上传成功',
        'file_path': file_path
    })

@app.route('/course/<course_name>/publish_work', methods=['POST'])
def publish_work(course_name):
    if 'username' not in session:
        return jsonify({'success': False, 'message': '请先登录'})
        
    homework_type = request.form.get('homework_type')
    title = request.form.get('title')
    description = request.form.get('content')
    deadline = request.form.get('deadline')
    publish_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print(publish_time)
    print('deadline:', deadline)
    # 数据验证
    if not all([homework_type, title, description, deadline]):
        return jsonify({
            'success': False, 
            'message': '请填写所有必填项'
        })
    
    try:
        deadline = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
        attachment_path = None
        file = request.files['attachment']
        if file.filename != '':
            homework_folder = os.path.join(
                app.config['UPLOAD_FOLDER'],
                course_name,
                title
            )
            os.makedirs(homework_folder, exist_ok=True)
            attachment_path = os.path.join(homework_folder, file.filename)
            file.save(attachment_path)
            print(f'path: {attachment_path}')
        
        if attachment_path:  # 只取load/后的内容
            attachment_path = os.path.relpath(attachment_path, app.config['UPLOAD_FOLDER'])

        # TODO: 添加数据库操作
        # parameters: course_name, homework_type, title, description, deadline, publish_time [, attachment_path]
        # deadline format: %Y-%m-%dT%H:%M
        # publish_time format: %Y-%m-%dT%H:%M:%S
        
        
        
        return jsonify({
            'success': True,
            'message': '作业发布成功'
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'success': False,
            'message': '发布失败，请稍后重试'
        })


# 公告看看做不做
@app.route('/course/<course_name>/publish_announcement', methods=['POST'])
def publish_announcement(course_name):
    if 'username' not in session:
        return redirect(url_for('login'))
        
    content = request.form.get('content')
    if content:
        print(f"公告: {content}")
        return jsonify({
            'status': 'success',
            'message': '公告发布成功!',
        })
    
    return jsonify({
        'status': 'error',
        'message': '公告内容不能为空'
    }), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
