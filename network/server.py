# -*- coding: utf-8 -*-
from sensors import SensorManager
from ai.predict import Predict
from database.connect import insert_env_data, select_env_data
from . import app, global_frame, lock # 导入全局帧和锁
from flask import jsonify
import random

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

        # --- 从全局缓存拿图，不碰硬件驱动 ---
        current_img = None
        with lock:
            if global_frame is not None:
                current_img = global_frame.copy()
        
        pests_list = []
        if current_img is not None:
            pests_list = ai_engine.analyze(current_img)
            print(f"🧠 [后台AI] 识别到: {pests_list}")
        else:
            print("⚠️ 警告：当前未捕获到画面，跳过识别")
        
        # 统计
        aphid_count = pests_list.count("蚜虫")
        armyworm_count = pests_list.count("粘虫")
        beetle_count = pests_list.count("瓢虫") + pests_list.count("天牛") + pests_list.count("甲虫")

        insert_env_data(temperature, humidity, soil, light, ph, 
                        aphid_count, armyworm_count, beetle_count)
        
        return {"aphid": aphid_count, "beetle": beetle_count} # 简版返回
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
        "ph": float(row[4]) if row[4] else 0,
        "aphid": int(row[5]) if row[5] else 0,
        "armyworm": int(row[6]) if row[6] else 0,
        "beetle": int(row[7]) if row[7] else 0,
    })