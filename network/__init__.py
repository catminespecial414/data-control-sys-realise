# -*- coding: utf-8 -*-
import time
import random
import threading
from flask import jsonify
from ai.predict import Predict
from database.connect import insert_env_data, select_env_data
from . import app, lock, state 

ai_engine = Predict()

def execute_analysis_and_save():
    # 1. 模拟环境数据 (移除 DHT11 物理读取)
    t, h, s = round(random.uniform(20, 30), 1), round(random.uniform(40, 70), 1), round(random.uniform(20, 40), 1)
    l, p = random.randint(300, 800), 7.0

    # 2. 获取画面并 AI 识别
    aphid, armyworm, beetle = 0, 0, 0
    current_img = None
    with lock:
        if state.get('frame') is not None:
            current_img = state['frame'].copy()
    
    if current_img is not None:
        try:
            res = ai_engine.analyze(current_img)
            if isinstance(res, list):
                aphid, armyworm = res.count("蚜虫"), res.count("粘虫")
                beetle = res.count("瓢虫") + res.count("天牛")
            print(f"✅ [AI] 识别成功")
        except: pass
    else:
        print("ℹ️ [System] 等待画面缓存...")

    # 3. 写入数据库
    try:
        insert_env_data(t, h, s, l, p, aphid, armyworm, beetle)
        print(f"💾 [Database] 数据已保存: T:{t} H:{h}")
    except Exception as e:
        # 这里如果报错 'con' is not defined，说明你的 database/connect.py 脚本里有错
        print(f"❌ [Database Error] {e}")

def auto_recognition_task():
    print("[System] 后台任务已启动...")
    while True:
        execute_analysis_and_save()
        time.sleep(15)

# 启动后台线程 (增加判断防止重复启动)
if not any(t.name == "AI_Task" for t in threading.enumerate()):
    threading.Thread(target=auto_recognition_task, name="AI_Task", daemon=True).start()

# --- 这里只保留前端图表需要的 JSON 数据接口 ---
@app.route('/chart')
def chart_data_api():
    row = select_env_data()
    if row:
        return jsonify({
            "temperature": float(row[0]), "humidity": float(row[1]),
            "soil": float(row[2]), "light": int(row[3]), "ph": float(row[4]),
            "aphid": int(row[5]), "armyworm": int(row[6]), "beetle": int(row[7]),
        })
    return jsonify({"status": "no_data"}), 200