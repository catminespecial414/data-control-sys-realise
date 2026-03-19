# -*- coding: utf-8 -*-
import time
import cv2
import threading
from flask import Flask, render_template, session, Response, request, redirect, url_for

app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")
app.secret_key = '6666'
username = 'admin'

# --- 摄像头全局初始化 ---
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# 全局共享变量与锁
global_frame = None
lock = threading.Lock()

def capture_thread():
    """独占线程：唯一的摄像头读取入口"""
    global global_frame
    while True:
        success, frame = camera.read()
        if success:
            with lock:
                global_frame = frame.copy()
        else:
            time.sleep(0.1)

# 启动采集线程
t = threading.Thread(target=capture_thread, daemon=True)
t.start()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('user_id')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/')
def index():
    if 'user' not in session: return redirect('/login')
    return render_template("index.html", username=username)

def gen_frames():
    """视频流：直接从内存 global_frame 拿图，不碰硬件"""
    while True:
        with lock:
            if global_frame is None:
                continue
            ret, buffer = cv2.imencode('.jpg', global_frame)
        
        if not ret: continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        time.sleep(0.04) # 限制帧率，减轻系统压力

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 导入业务逻辑
from . import server