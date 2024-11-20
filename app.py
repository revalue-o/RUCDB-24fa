# from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import markdown
import os
import time
os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = secrets.token_hex(16)
#登录部分，负责人杜海乐
@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 简单的验证逻辑
        if (username == 'admin' or username == 'student') and password == 'password':
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password!'
            return render_template('login.html', error=error)

    return render_template('login.html')

# @app.route('/welcome')
# def welcome():
#     username = request.args.get('username', 'Guest')
#     return f"<h1>Welcome, {username}!</h1>"
#登录部分结束


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
    {'name': f'ppt{i}', 'date': '2024-11-19 22:44:46'} for i in range(15)
]

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    print(f"home current_username: {session['username']}")
    return render_template('home.html', courses=courses, items=items, upload=upload)

@app.route('/course/<string:course_name>')
def course(course_name):
    print(f"course current_username: {session['username']}")
    time.sleep(3)
    return render_template('course_main.html', courses=courses, course_name=course_name)

@app.route('/Cwork')
def Cwork():
    return render_template('course_work.html', courses=courses, work_outline=work_outline)

@app.route('/Csrc')
def Csrc():
    return render_template('course_src.html', courses=courses, files=files)

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