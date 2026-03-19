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
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1) 

state = {
    'frame': None
}

lock = threading.Lock()

def capture_worker():
    # 强制等待 2 秒，让硬件完成上电和曝光初始化
    time.sleep(2) 
    print(" [Hardware] 摄像头硬件就绪")
    while True:
        success, frame = camera.read()
        if success:
            with lock:
                state['frame'] = frame
        else:
            print(" [Hardware] 读取失败，尝试重置驱动...")
            time.sleep(1)
        time.sleep(0.04) # 稍微快一点点，保持画面流畅

# 启动线程前先打印
print(" [System] 正在启动摄像头采集线程...")
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
        with lock:
            img = state.get('frame')
        
        if img is None:
            # 如果没画面，千万不要报错，直接多睡一会
            time.sleep(0.5)
            continue
            
        try:
            ret, buffer = cv2.imencode('.jpg', img)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except Exception as e:
            print(f"[Stream Error] {e}")
            
        time.sleep(0.08) # 保持约 12 帧，对树莓派最友好

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

from . import server