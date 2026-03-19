# -*- coding: utf-8 -*-
import time
import random
import threading
from flask import jsonify, render_template
from ai.predict import Predict
from database.connect import insert_env_data, select_env_data
# 导入共享的 state 字典、lock 和 app
from . import app, lock, state 

# 初始化 AI 引擎 (不再初始化 SensorManager)
ai_engine = Predict()

def execute_analysis_and_save():
    """纯 AI + 模拟环境数据逻辑 (回滚版)"""
    
    # 1. 模拟环境数据 (恢复到稳定状态)
    t = round(random.uniform(20, 30), 1)
    h = round(random.uniform(40, 70), 1)
    s = round(random.uniform(20, 40), 1)      
    l = random.randint(300, 800)
    p = 7.0

    # 2. 从共享字典获取当前画面
    aphid, armyworm, beetle = 0, 0, 0
    current_img = None
    with lock:
        if state['frame'] is not None:
            current_img = state['frame'].copy()
    
    # 3. AI 识别
    if current_img is not None:
        try:
            res = ai_engine.analyze(current_img)
            if isinstance(res, list):
                aphid = res.count("蚜虫")
                armyworm = res.count("粘虫")
                beetle = res.count("瓢虫") + res.count("天牛") + res.count("甲虫")
            print(f"✅ [AI] 识别成功：Pests:{aphid+armyworm+beetle}")
        except Exception as e:
            print(f"⚠️ [AI Error] {e}")
    else:
        print("ℹ️ [System] 等待摄像头画面中...")

    # 4. 存入数据库
    try:
        insert_env_data(t, h, s, l, p, aphid, armyworm, beetle)
        print(f"💾 [Database] 模拟数据已存入：T:{t} H:{h}")
    except Exception as e:
        print(f"❌ [Database Error] {e}")

def auto_recognition_task():
    print("[System] 后台任务启动 (已移除 DHT11 物理读取)")
    while True:
        execute_analysis_and_save()
        time.sleep(15)

# 启动后台线程
daemon_thread = threading.Thread(target=auto_recognition_task, daemon=True)
daemon_thread.start()

# --- 核心路由定义 (确保网页不报 404) ---

@app.route("/chart")
def chart_data_api():
    row = select_env_data()
    if row:
        return jsonify({
            "temperature": float(row[0]),
            "humidity": float(row[1]),
            "soil": float(row[2]),
            "light": int(row[3]),
            "ph": float(row[4]),
            "aphid": int(row[5]),
            "armyworm": int(row[6]),
            "beetle": int(row[7]),
        })
    return jsonify({"status": "waiting"}), 200

@app.route("/chart_page")
def chart_page():
    return render_template("chart.html")

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")