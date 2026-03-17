# -*- coding: utf-8 -*-
from database.connect import insert_env_data
from . import app
from flask import jsonify
import random

def read_sensor():
    temperature = round(random.uniform(20,30),2)
    humidity = round(random.uniform(40,70),2)

    # 写入数据库
    insert_env_data(temperature, humidity)
    return temperature, humidity

# 温湿度
@app.route("/chart")
def chart():
    temperature, humidity = read_sensor()
    return jsonify({
        "temperature": temperature,
        "humidity": humidity
    })


# 农田数据
@app.route("/farm")
def farm():
    return jsonify({
        "soil": round(random.uniform(30,70),2),
        "light": random.randint(200,800),
        "ph": round(random.uniform(5.5,7.5),2)
    })


# 害虫数据
@app.route("/pest")
def pest():
    return jsonify({
        "aphid": random.randint(0,20),
        "armyworm": random.randint(0,15),
        "beetle": random.randint(0,10)
    })