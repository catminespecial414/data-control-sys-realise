# -*- coding: utf-8 -*-
from sensors import SensorManager
from ai.predict import Predict
from database.connect import insert_env_data, select_env_data
from . import app, camera  # 关键：从 __init__ 导入全局 camera
from flask import jsonify
import random
import cv2

sensor_manager = SensorManager()
ai_engine = Predict()

def write_all_data():
    try:
        sensor_data = sensor_manager.get_all_data()
        temperature = sensor_data.get('temperature', 0)
        humidity = sensor_data.get('humidity', 0)
        soil = round(random.uniform(30, 70), 2)
        light = random.randint(200, 800)
        ph = round(random.uniform(5.5, 7.5), 2)

        # --- 【主动抓帧识别】 ---
        # 即使没人看视频，我们也从 camera 抓一帧给 AI
        success, frame = camera.read()
        pests_list = []
        if success:
            pests_list = ai_engine.analyze(frame)
            print(f"🧠 [后台AI] 识别到: {pests_list}")
        
        # 统计
        aphid_count = pests_list.count("蚜虫")
        armyworm_count = pests_list.count("粘虫")
        beetle_count = pests_list.count("瓢虫") + pests_list.count("天牛") + pests_list.count("甲虫")

        insert_env_data(temperature, humidity, soil, light, ph, 
                        aphid_count, armyworm_count, beetle_count)
        
        return {
            "temperature": temperature, "humidity": humidity, "soil": soil,
            "light": light, "ph": ph, "aphid": aphid_count,
            "armyworm": armyworm_count, "beetle": beetle_count
        }
    except Exception as e:
        print(f"❌ server 写入异常: {e}")
        return {}

@app.route("/chart")
def chart():
    write_all_data()
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
