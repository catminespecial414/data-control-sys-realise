# -*- coding: utf-8 -*-
import time
import cv2
import threading
from flask import Flask, render_template, session, Response, request, redirect, url_for

# [1] 初始化 Flask 实例
app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")
app.secret_key = '6666'

# [2] 定义全局共享变量
state = {'frame': None}
lock = threading.Lock()

# [3] 摄像头硬件采集逻辑
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def capture_worker():
    time.sleep(2)
    print("📸 [Hardware] 摄像头硬件已就绪")
    while True:
        success, frame = camera.read()
        if success:
            with lock:
                state['frame'] = frame
        else:
            time.sleep(1)
        time.sleep(0.04)

print("🚀 [System] 正在启动摄像头采集线程...")
threading.Thread(target=capture_worker, daemon=True).start()

# [4] 页面跳转路由 (仅负责返回 HTML)
@app.route('/')
@app.route('/dashboard')
def index():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template("index.html", username='admin')

@app.route('/chart_page')
def chart_page():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template("chart.html", username='admin')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('user_id')
        return redirect(url_for('index'))
    return render_template('login.html')

def gen_frames():
    while True:
        with lock:
            img = state.get('frame')
        if img is None:
            time.sleep(0.5)
            continue
        ret, buffer = cv2.imencode('.jpg', img)
        if ret:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        time.sleep(0.08)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# [5] 最后导入后台业务模块
from . import server