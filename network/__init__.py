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
    """全系统唯一的摄像头读取者"""
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

# 启动采集线程
t = threading.Thread(target=capture_worker, daemon=True)
t.start()

# --- 【核心修复】强制预热逻辑 ---
print("⏳ [System] 正在等待摄像头画面预热...")
max_tries = 20
while global_frame is None and max_tries > 0:
    time.sleep(0.5)
    max_tries -= 1
    print(f"   ...正在重试硬件握手 ({20-max_tries}/20)")

if global_frame is not None:
    print("✅ [System] 硬件就绪，画面已同步！")
else:
    print("❌ [System] 硬件启动超时，请检查摄像头连接。")

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

from . import server