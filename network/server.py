# -*- coding: utf-8 -*-
import time
import random
import threading
from flask import jsonify
from ai.predict import Predict
from database.connect import insert_env_data, select_env_data

# 从 __init__.py 导入已经初始化好的对象
from . import app, lock, state 

ai_engine = Predict()

def execute_analysis_and_save():
    # 1. 模拟环境数据
    t, h, s = round(random.uniform(20, 30), 1), round(random.uniform(40, 70), 1), round(random.uniform(20, 40), 1)
    l, p = random.randint(300, 800), 7.0

# 2. 执行 AI 逻辑
    beetle_count, ladybug_count, mantis_count = 0, 0, 0
    current_img = None
    with lock:
        if state.get('frame') is not None:
            current_img = state['frame'].copy()

    if current_img is not None:
        try:
            res = ai_engine.analyze(current_img)
            print(f" [AI Raw] 原始结果: {res}") 

            if isinstance(res, list):
                for item in res:
                    # 1. 甲虫类 (包含天牛、金龟子、锹甲等)
                    if item in ["甲虫", "天牛", "金龟子", "锹甲", "象鼻虫"]:
                        beetle_count += 1
                    
                    # 2. 瓢虫类 (包含各种瓢虫)
                    elif item in ["瓢虫", "七星瓢虫", "异色瓢虫"]:
                        ladybug_count += 1
                    
                    # 3. 螳螂类 (包含各种螳螂)
                    elif item in ["螳螂", "宽腹螳螂", "中华大刀螳"]:
                        mantis_count += 1
                    
                    else:
                        print(f"ℹ [Other] 发现其他生物: {item}")

            print(f" [Result] 分类统计 -> 甲虫:{beetle_count}, 瓢虫:{ladybug_count}, 螳螂:{mantis_count}")
        except Exception as e:
            print(f" [AI Error] {e}")

    try:
        insert_env_data(t, h, s, l, p, beetle_count, ladybug_count, mantis_count)
        print(f" [Database] 数据已保存")
    except Exception as e:
        print(f" [Database Error] {e}")

def auto_recognition_task():
    print("[System] 后台 AI 任务线程已启动...")
    while True:
        execute_analysis_and_save()
        time.sleep(15)

# 启动后台线程
if not any(t.name == "AI_Task" for t in threading.enumerate()):
    threading.Thread(target=auto_recognition_task, name="AI_Task", daemon=True).start()

@app.route('/chart')
def chart_data_api():
    try:
        row = select_env_data()
        if row:
            return jsonify({
                "temperature": float(row[0]), "humidity": float(row[1]),
                "soil": float(row[2]), "light": int(row[3]), "ph": float(row[4]),
                "aphid": int(row[5]), "armyworm": int(row[6]), "beetle": int(row[7]),
            })
    except: pass
    return jsonify({"status": "no_data"}), 200