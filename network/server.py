# -*- coding: utf-8 -*-
import time
import random
import threading
from flask import jsonify
from sensors import SensorManager
from ai.predict import Predict
from database.connect import insert_env_data, select_env_data
# 导入共享的 state 字典、lock 和 app
from . import app, lock, state 

# 初始化传感器和 AI 引擎
sensor_manager = SensorManager()
ai_engine = Predict()

def execute_analysis_and_save():
    
    # 1. 获取真实传感器数据 (现在会调用你的 DHT11 物理读取逻辑)
    sensor_data = sensor_manager.get_all_data()
    t = sensor_data.get('temperature', 0)
    h = sensor_data.get('humidity', 0)
    s = sensor_data.get('soil', 0)      
    l = sensor_data.get('light', 0)
    p = sensor_data.get('ph', 7.0)

    # 2. 从共享字典 state 中安全拷贝当前画面 (代码保持不变)
    current_img = None
    with lock:
        if state['frame'] is not None:
            current_img = state['frame'].copy()
            print(" [AI] 成功获取画面，准备识别物理环境...")
        else:
            print(" [AI] 等待画面缓存中...")
            return

    # 3. AI 识别逻辑 (代码保持不变)
    aphid, armyworm, beetle = 0, 0, 0
    try:
        res = ai_engine.analyze(current_img)
        aphid = res.count("蚜虫")
        armyworm = res.count("粘虫")
        beetle = res.count("瓢虫") + res.count("天牛") + res.count("甲虫")
        print(f" [Auto AI] 识别成功：蚜虫:{aphid}, 粘虫:{armyworm}, 甲虫:{beetle}")
    except Exception as e:
        print(f" [AI Error] 识别出错: {e}")
    
    # 4. 存入数据库
    insert_env_data(t, h, s, l, p, aphid, armyworm, beetle)
    print(f" [Database] 数据已保存：T:{t} H:{h} Pests:{aphid+armyworm+beetle}")

def auto_recognition_task():
    print("[System] AI 后台任务已进入循环...")
    while True:
        try:
            if state['frame'] is not None:
                
                time.sleep(1) 
                execute_analysis_and_save()
            else:
                print("[Debug] 等待画面中...") 
        except Exception as e:
            print(f"[Task Error] {e}")
        
        time.sleep(15)

daemon_thread = threading.Thread(target=auto_recognition_task, daemon=True)
daemon_thread.start()

@app.route("/chart")
def chart_data_api():
    """专门为 chart.html 提供的 API 接口"""
    # 从数据库获取最新的一条记录
    row = select_env_data()
    
    # 返回与前端 JS 匹配的 JSON 格式
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