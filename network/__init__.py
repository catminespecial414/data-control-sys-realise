# -*- coding: utf-8 -*-
# network/__init__.py
# 网络通信模块初始化
from ai.predict import Predict
pd = Predict()
import time
from flask import Flask, render_template, session, Response
import cv2
from flask import request, redirect, url_for

from database.connect import select_user, select_device, alter_user

app = Flask(
    __name__,
    template_folder="../web/templates",
    static_folder="../web/static",
)
app.secret_key= '6666'
global username
username = 'admin'

camera = cv2.VideoCapture(0)

#登录页

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
#TODO:加载摄像头
def gen_frames():
    last_ai_time = 0  # 记录上次 AI 识别的时间
    while True:
        success, frame = camera.read()
        # print("read:", success) # 如果觉得终端太乱，可以把这行注释掉

        if not success:
            continue

        # --- 每 2-3 秒进行一次真实 AI 识别，防止 API 频率过快 ---
        now = time.time()
        if now - last_ai_time > 3: 
            # 传入当前的真实画面 frame 给 AI 
            pd.analyze(frame) 
            last_ai_time = now
            print("[AI] 正在分析当前画面...")

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame_data = buffer.tobytes()
        # print("yielding frame") # 同理，正常运行后可以注释掉

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# 导入 API
from . import server