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
    """读取传感器 -> 从共享字典获取图片 -> AI 识别 -> 写入数据库"""
    
    # 1. 采集环境数据
    sensor_data = sensor_manager.get_all_data()
    t = sensor_data.get('temperature', 0)
    h = sensor_data.get('humidity', 0)
    # 模拟其他传感器数据
    s, l, p = round(random.uniform(30, 70), 2), random.randint(200, 800), round(random.uniform(5.5, 7.5), 2)

    # 2. 从共享字典 state 中安全拷贝当前画面
    current_img = None
    with lock:
        if state['frame'] is not None:
            current_img = state['frame'].copy()
            print("📸 [AI] 成功获取共享画面，准备识别...")
        else:
            print("⚠️ [AI] 字典中的 frame 依然为空，无法识别")
            return

    # 3. AI 害虫识别逻辑
    aphid, armyworm, beetle = 0, 0, 0
    try:
        # 执行推理
        res = ai_engine.analyze(current_img)
        # 统计识别结果中的害虫数量（需确保 Predict.analyze 返回的是包含中文类名的列表）
        aphid = res.count("蚜虫")
        armyworm = res.count("粘虫")
        beetle = res.count("瓢虫") + res.count("天牛") + res.count("甲虫")
        print(f"📊 [Auto AI] 识别成功：蚜虫:{aphid}, 粘虫:{armyworm}, 甲虫:{beetle}")
    except Exception as e:
        print(f"❌ [AI Error] 识别过程出错: {e}")
    
    # 4. 存入数据库
    insert_env_data(t, h, s, l, p, aphid, armyworm, beetle)

def auto_recognition_task():
    print("⏲️ [System] AI 后台任务已进入循环...")
    while True:
        try:
            if state['frame'] is not None:
                
                time.sleep(1) 
                execute_analysis_and_save()
            else:
                print("⚠️ [Debug] 等待画面中...") 
        except Exception as e:
            print(f"⚠️ [Task Error] {e}")
        
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