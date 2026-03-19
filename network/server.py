# -*- coding: utf-8 -*-
import time
import random
import threading
from flask import jsonify
from sensors import SensorManager
from ai.predict import Predict
from database.connect import insert_env_data, select_env_data
from . import app, global_frame, lock

sensor_manager = SensorManager()
ai_engine = Predict()

def auto_recognition_task():
    """后台定时任务：每 10 秒自动存库一次"""
    while True:
        try:
            if global_frame is not None:
                execute_analysis_and_save()
        except Exception as e:
            print(f"⚠️ [Task Error] {e}")
        time.sleep(10)

def execute_analysis_and_save():
    sensor_data = sensor_manager.get_all_data()
    t, h = sensor_data.get('temperature', 0), sensor_data.get('humidity', 0)
    s, l, p = round(random.uniform(30,70),2), random.randint(200,800), round(random.uniform(5.5,7.5),2)

    current_img = None
    with lock:
        if global_frame is not None:
            current_img = global_frame.copy()

    aphid, armyworm, beetle = 0, 0, 0
    if current_img is not None:
        res = ai_engine.analyze(current_img)
        aphid = res.count("蚜虫")
        armyworm = res.count("粘虫")
        beetle = res.count("瓢虫") + res.count("天牛") + res.count("甲虫")
        print(f"📊 [Auto AI] 数据更新：蚜虫:{aphid}, 甲虫:{beetle}")
    
    insert_env_data(t, h, s, l, p, aphid, armyworm, beetle)

# 启动后台线程
threading.Thread(target=auto_recognition_task, daemon=True).start()

@app.route("/chart")
def chart():
    """这是给前端提供 JSON 数据的 API"""
    row = select_env_data()
    return jsonify({
        "temperature": float(row[0]) if row[0] else 0,
        "humidity": float(row[1]) if row[1] else 0,
        "soil": float(row[2]) if row[2] else 0,
        "light": int(row[3]) if row[3] else 0,
        "ph": float(row[4]) if row[4] else 0,
        "aphid": int(row[5]) if row[5] else 0,
        "armyworm": int(row[6]) if row[6] else 0,
        "beetle": int(row[7]) if row[7] else 0,
    })