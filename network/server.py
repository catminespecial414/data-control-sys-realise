# -*- coding: utf-8 -*-
from database.connect import insert_env_data, select_env_data
from . import app
from flask import jsonify
import random

def write_all_data():
    temperature = round(random.uniform(20, 30), 2)
    humidity = round(random.uniform(40, 70), 2)
    soil = round(random.uniform(30, 70), 2)
    light = random.randint(200, 800)
    ph = round(random.uniform(5.5, 7.5), 2)

    aphid = random.randint(0, 20)
    armyworm = random.randint(0, 15)
    beetle = random.randint(0, 10)

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
