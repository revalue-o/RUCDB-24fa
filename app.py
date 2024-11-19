# from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for
import markdown
import os
os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#登录部分，负责人杜海乐
@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 简单的验证逻辑
        if username == 'admin' and password == 'password':
            return redirect(url_for('home', username=username))
        else:
            error = 'Invalid username or password!'
            return render_template('login.html', error=error)

    return render_template('login.html')

# @app.route('/welcome')
# def welcome():
#     username = request.args.get('username', 'Guest')
#     return f"<h1>Welcome, {username}!</h1>"
#登录部分结束
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

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