# -*- coding: utf-8 -*-
import time
import cv2
import threading
from flask import Flask, render_template, session, Response, request, redirect, url_for

app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")
app.secret_key = '6666' #

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1) #

global_frame = None
lock = threading.Lock()

# 使用字典来存储，确保跨模块引用时地址不变
state = {
    'frame': None
}

def capture_worker():
    global state
    while True:
        success, frame = camera.read()
        if success:
            with lock:
                state['frame'] = frame.copy() # 更新字典里的值
        else:
            time.sleep(0.2)
        time.sleep(0.01)

threading.Thread(target=capture_worker, daemon=True).start()


@app.route('/')
@app.route('/dashboard')
def index():
    """主界面：包含摄像头预览 (index.html)"""
    if 'user' not in session: return redirect(url_for('login'))
    return render_template("index.html", username='admin') #

@app.route('/chart_page')
def chart_page():
    """图表页：展示详细数据图表 (chart.html)"""
    if 'user' not in session: return redirect(url_for('login'))
    return render_template("chart.html", username='admin') #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('user_id')
        return redirect(url_for('index'))
    return render_template('login.html')

def gen_frames():
    while True:
        time.sleep(0.1) 
        
        with lock:
            img = state.get('frame')
            
        if img is None:
            continue
        ret, buffer = cv2.imencode('.jpg', img)
        if ret:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

from . import server