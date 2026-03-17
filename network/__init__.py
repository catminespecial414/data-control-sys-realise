# -*- coding: utf-8 -*-
# network/__init__.py
# 网络通信模块初始化
from flask import Flask, render_template, session

from database.connect import select_user, select_device, alter_user

app = Flask(
    __name__,
    template_folder="../web/templates",
    static_folder="../web/static",
)
app.secret_key= '6666'
global username
username = 'admin'
#登录页
from flask import request, render_template, redirect, url_for

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')   # TODO
        # TODO:需要从数据库替换该名字
        user = select_user(user_id)
        password = request.form.get('password') # TODO
        session['user'] = user_id

        # TODO: 查询数据库
        if user and int(user["userid"]) == int(user_id) and int(user["password"]) == int(password):
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="账号或密码错误")

    return render_template('login.html')
# 首页
@app.route('/')
def index():
    # 未登录会跳转到登录页面
    if 'user' not in session:
        return redirect('/login')
    # TODO: 从数据库算农田评分
    farm_score = 85

    # TODO: 从数据库查设备状态
    devices = select_device()

    return render_template("index.html",
                           farm_score=farm_score,
                           devices=devices,
                           username=username)

@app.route("/dashboard")
def dashboard():
    return render_template('index.html')
# 图表页
@app.route("/chart_page")
def chart_page():
    return render_template("chart.html", username=username)

#用户页
@app.route("/setting")
def setting():
    return render_template("setting.html", username= username)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for('index'))

@app.route("/setUser", methods=['GET','POST'])
def set_user():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user_name = request.form.get('name')
        user_password = request.form.get('password')
        alter_user(user_id, user_name, user_password)
        session['user'] = select_user(user_id)

    return redirect(url_for('index'))


# 导入 API
from . import server