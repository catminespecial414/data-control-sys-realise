# -*- coding: utf-8 -*-
import time
import cv2
import os
from flask import Flask, render_template, session, Response, request, redirect, url_for
from ai.predict import Predict
from database.connect import select_user, select_device, alter_user

# 初始化 Flask
app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")
app.secret_key = '6666'
username = 'admin'

# --- 摄像头兼容性初始化 ---
# 解决 TypeError: VideoCapture() takes at most 1 argument
camera = cv2.VideoCapture(0) 

# 设置硬件参数（针对树莓派优化，防止 VIDIOC_QBUF 报错）
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG')) # 强制压缩格式
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1) # 核心：限制缓冲区为1，解决卡顿和报错
camera.set(cv2.CAP_PROP_FPS, 20)      # 限制帧率

# 初始化 AI 引擎
pd = Predict()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = select_user(user_id)
        password = request.form.get('password')
        session['user'] = user_id
        if user and int(user["userid"]) == int(user_id) and int(user["password"]) == int(password):
            return redirect(url_for('index'))
        return render_template('login.html', error="账号或密码错误")
    return render_template('login.html')

@app.route('/')
def index():
    if 'user' not in session: return redirect('/login')
    devices = select_device()
    return render_template("index.html", farm_score=85, devices=devices, username=username)

def gen_frames():
    """视频流生成器：同时触发 AI 识别"""
    last_ai_time = 0
    while True:
        success, frame = camera.read()
        if not success:
            time.sleep(0.1) 
            continue

        # 每 3 秒执行一次 AI 识别
        now = time.time()
        if now - last_ai_time > 3:
            try:
                pd.analyze(frame) # 传入当前帧给 AI
                last_ai_time = now
                print("🧠 [AI] 实时分析已触发...")
            except Exception as e:
                print(f"⚠️ AI 调用失败: {e}")

        # 编码并推送
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret: continue
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/chart_page")
def chart_page(): return render_template("chart.html", username=username)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# 导入业务逻辑
from . import server