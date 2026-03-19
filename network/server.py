# -*- coding: utf-8 -*-
from sensors import SensorManager
from ai.predict import Predict
from database.connect import insert_env_data, select_env_data
from . import app, global_frame, lock # 关键：导入全局变量和锁
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

        # --- 从内存共享变量中安全拿图 ---
        current_img = None
        with lock:
            if global_frame is not None:
                current_img = global_frame.copy()
        
        pests_list = []
        if current_img is not None:
            # 执行 AI 识别
            pests_list = ai_engine.analyze(current_img)
            print(f"🧠 [AI 分析] 识别结果: {pests_list}")
        else:
            print("⚠️ 画面尚未准备好，跳过此次 AI 识别")
        
        # 统计数量 (int)
        aphid = pests_list.count("蚜虫")
        armyworm = pests_list.count("粘虫")
        beetle = pests_list.count("瓢虫") + pests_list.count("天牛") + pests_list.count("甲虫")

        # 写入数据库
        insert_env_data(temperature, humidity, soil, light, ph, aphid, armyworm, beetle)
        
        return {
            "temperature": temperature, "humidity": humidity, "soil": soil,
            "light": light, "ph": ph, "aphid": aphid,
            "armyworm": armyworm, "beetle": beetle
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