# -*- coding: utf-8 -*-
# from sensors import SensorManager
from ai import Predict
from database.connect import insert_env_data, select_env_data
from . import app
from flask import jsonify
import random

sensor_manager = SensorManager()
ai_engine = Predict()

def write_all_data():
    sensor_data = sensor_manager.get_all_data()
    temperature = sensor_data.get('temperature', 0)
    humidity = sensor_data.get('humidity', 0)
    soil = round(random.uniform(30, 70), 2)
    light = random.randint(200, 800)
    ph = round(random.uniform(5.5, 7.5), 2)
    pests = ai_engine.analyze()
    aphid = pests.count("aphid")       # 蚜虫
    armyworm = pests.count("armyworm") # 粘虫
    beetle = pests.count("beetle")     # 甲虫

    # temperature = round(random.uniform(20, 30), 2)
    # humidity = round(random.uniform(40, 70), 2)
    # soil = round(random.uniform(30, 70), 2)
    # light = random.randint(200, 800)
    # ph = round(random.uniform(5.5, 7.5), 2)
    # aphid = round(random.uniform(5.5, 7.5), 2)
    # armyworm = round(random.uniform(5.5, 7.5), 2)
    # beetle = round(random.uniform(5.5, 7.5), 2)

    insert_env_data(temperature, humidity, soil, light, ph, aphid, armyworm, beetle)
    return {
        "temperature": temperature,
        "humidity": humidity,
        "soil": soil,
        "light": light,
        "ph": ph,
        "aphid": aphid,
        "armyworm": armyworm,
        "beetle": beetle,
    }

# 温湿度
@app.route("/chart")
def chart():
    write_all_data()
    row = select_env_data()
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
