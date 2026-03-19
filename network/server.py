# -*- coding: utf-8 -*-
import time
import random
from flask import jsonify
from sensors import SensorManager
from ai.predict import Predict
from database.connect import insert_env_data, select_env_data
from . import app, global_frame, lock

sensor_manager = SensorManager()
ai_engine = Predict()

def write_all_data():
    """执行 AI 识别并存入数据库"""
    try:
        # 1. 采集环境数据
        sensor_data = sensor_manager.get_all_data()
        t = sensor_data.get('temperature', 0)
        h = sensor_data.get('humidity', 0)
        s, l, p = round(random.uniform(30,70),2), random.randint(200,800), round(random.uniform(5.5,7.5),2)

        # 2. 抓取当前内存帧
        current_img = None
        with lock:
            if global_frame is not None:
                current_img = global_frame.copy()

        aphid, armyworm, beetle = 0, 0, 0
        if current_img is not None:
            # 这里的 analyze 会返回一个列表
            res = ai_engine.analyze(current_img)
            aphid = res.count("蚜虫")
            armyworm = res.count("粘虫")
            beetle = res.count("瓢虫") + res.count("天牛") + res.count("甲虫")
            print(f"📊 [AI Output] 蚜虫:{aphid}, 粘虫:{armyworm}, 甲虫:{beetle}")
        else:
            print("⚠️ [Warning] AI 无法获取当前帧，跳过识别")

        # 3. 写入数据库
        insert_env_data(t, h, s, l, p, aphid, armyworm, beetle)
        return True
    except Exception as e:
        print(f"❌ [Database Error] {e}")
        return False

@app.route("/chart")
def chart():
    # 每次请求 chart 数据时触发一次识别并入库
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