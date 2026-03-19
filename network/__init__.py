# -*- coding: utf-8 -*-
import time
import cv2
import threading
from flask import Flask, render_template, session, Response, request, redirect, url_for

app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")
app.secret_key = '6666'

# --- 摄像头单例初始化 ---
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

global_frame = None
lock = threading.Lock()

def capture_worker():
    global global_frame
    print("🚀 [System] 硬件采集线程启动...")
    while True:
        success, frame = camera.read()
        if success:
            with lock:
                global_frame = frame.copy()
        else:
            time.sleep(0.2)
        time.sleep(0.01)

t = threading.Thread(target=capture_worker, daemon=True)
t.start()

# --- 路由部分 ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('user_id')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/')
def index():
    if 'user' not in session: return redirect('/login')
    return render_template("index.html", username='admin')

@app.route("/dashboard")
def dashboard():
    """这是前端页面点击跳转的目标路由"""
    if 'user' not in session: 
        return redirect(url_for('login'))
    # 确保你的 HTML 文件名确实是 chart.html
    return render_template("chart.html", username='admin')
def gen_frames():
    while True:
        with lock:
            if global_frame is None: continue
            ret, buffer = cv2.imencode('.jpg', global_frame)
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        time.sleep(0.05)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# 导入业务接口
from . import server