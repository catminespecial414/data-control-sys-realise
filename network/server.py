# -*- coding: utf-8 -*-
import time
import random
import threading
from flask import jsonify
from sensors import SensorManager
from ai.predict import Predict
from database.connect import insert_env_data, select_env_data
from . import app, global_frame, lock

# 初始化传感器和 AI 引擎
sensor_manager = SensorManager()
ai_engine = Predict()

def auto_recognition_task():
    print("⏲️ [Debug] AI 后台任务已进入循环...") # 添加此行
    while True:
        try:
            if global_frame is not None:
                execute_analysis_and_save()
            else:
                # 如果一直打印这个，说明摄像头画面没传过来
                print("⚠️ [Debug] global_frame 还是 None，AI 无法工作") 
        except Exception as e:
            print(f"⚠️ [Task Error] {e}")
        time.sleep(10)
def execute_analysis_and_save():
    """读取传感器 -> AI 识别图片 -> 写入数据库"""
    # 1. 采集环境数据
    sensor_data = sensor_manager.get_all_data()
    t = sensor_data.get('temperature', 0)
    h = sensor_data.get('humidity', 0)
    # 模拟其他暂无硬件的传感器数据
    s, l, p = round(random.uniform(30, 70), 2), random.randint(200, 800), round(random.uniform(5.5, 7.5), 2)

    # 2. 从内存锁中拷贝当前画面
    current_img = None
    with lock:
        if global_frame is not None:
            current_img = global_frame.copy()

    # 3. AI 害虫识别
    aphid, armyworm, beetle = 0, 0, 0
    if current_img is not None:
        res = ai_engine.analyze(current_img)
        # 统计识别结果中的害虫数量
        aphid = res.count("蚜虫")
        armyworm = res.count("粘虫")
        beetle = res.count("瓢虫") + res.count("天牛") + res.count("甲虫")
        print(f"📊 [Auto AI] 识别成功：蚜虫:{aphid}, 粘虫:{armyworm}, 甲虫:{beetle}")
    
    # 4. 存入数据库
    insert_env_data(t, h, s, l, p, aphid, armyworm, beetle)


daemon_thread = threading.Thread(target=auto_recognition_task, daemon=True)
daemon_thread.start()

@app.route("/chart")
def chart_data_api():
    """这是专门给 chart.html 里的 JS 脚本提供数据的接口"""
   
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