# -*- coding: utf-8 -*-
import time
import cv2
import threading
from flask import Flask, render_template, session, Response, request, redirect, url_for

# ==========================================================
# 1. 核心定义：必须在所有路由 (@app.route) 之前
# ==========================================================
app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")
app.secret_key = '6666'

# 共享状态字典和线程锁，供 server.py 调用
state = {
    'frame': None
}
lock = threading.Lock()

# ==========================================================
# 2. 硬件初始化：摄像头采集线程
# ==========================================================
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def capture_worker():
    """后台摄像头采集函数"""
    time.sleep(2)  # 给硬件曝光初始化时间
    print("📸 [Hardware] 摄像头硬件就绪")
    while True:
        success, frame = camera.read()
        if success:
            with lock:
                state['frame'] = frame
        else:
            print("⚠️ [Hardware] 读取失败，尝试重置驱动...")
            time.sleep(1)
        time.sleep(0.04) # 约 25 帧

print("🚀 [System] 正在启动摄像头采集线程...")
threading.Thread(target=capture_worker, daemon=True).start()

# ==========================================================
# 3. 基础页面路由：负责 HTML 渲染
# ==========================================================

@app.route('/')
@app.route('/dashboard')
def index():
    """主界面"""
    if 'user' not in session: return redirect(url_for('login'))
    return render_template("index.html", username='admin')

@app.route('/chart_page')
def chart_page():
    """图表详情页"""
    if 'user' not in session: return redirect(url_for('login'))
    return render_template("chart.html", username='admin')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录逻辑"""
    if request.method == 'POST':
        session['user'] = request.form.get('user_id')
        return redirect(url_for('index'))
    return render_template('login.html')

def gen_frames():
    """视频流生成器"""
    while True:
        with lock:
            img = state.get('frame')
        
        if img is None:
            time.sleep(0.5)
            continue
            
        try:
            ret, buffer = cv2.imencode('.jpg', img)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except Exception as e:
            print(f"❌ [Stream Error] {e}")
            
        time.sleep(0.08)

@app.route('/video_feed')
def video_feed():
    """视频流接口"""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# ==========================================================
# 4. 最后一步：导入后台任务模块
# ==========================================================
# 此时 app, lock, state 已经全部定义完成，server.py 可以安全引用它们
from . import server