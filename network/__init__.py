# -*- coding: utf-8 -*-
import time
import random
import threading
from flask import jsonify
from ai.predict import Predict
from database.connect import insert_env_data, select_env_data



# 初始化引擎
ai_engine = Predict()

def execute_analysis_and_save():
    """读取模拟数据 + AI识别 -> 存入数据库"""
    
    # 1. 模拟环境数据 (确保数据类型为数值，方便数据库写入)
    t = round(random.uniform(20.0, 30.0), 1)
    h = round(random.uniform(40.0, 70.0), 1)
    s = round(random.uniform(20.0, 40.0), 1)      
    l = random.randint(300, 800)
    p = 7.0

    # 2. 获取画面并执行 AI
    aphid, armyworm, beetle = 0, 0, 0
    current_img = None
    
    with lock:
        if state.get('frame') is not None:
            current_img = state['frame'].copy()
    
    if current_img is not None:
        try:
            res = ai_engine.analyze(current_img)
            # 增加类型检查，防止 res 不是列表导致 count 崩溃
            if isinstance(res, list):
                aphid = res.count("蚜虫")
                armyworm = res.count("粘虫")
                # 合并计算甲虫类
                beetle = res.count("瓢虫") + res.count("天牛") + res.count("甲虫")
            print(f"✅ [AI] 识别完成，害虫总数: {aphid + armyworm + beetle}")
        except Exception as e:
            print(f"⚠️ [AI Error] 识别过程异常: {e}")
    else:
        print("ℹ️ [System] 摄像头画面尚未就绪，跳过本次 AI 分析")

    # 3. 写入数据库 (增加强制类型转换，防止 None 值注入)
    try:
        insert_env_data(
            float(t), float(h), float(s), 
            int(l), float(p), 
            int(aphid), int(armyworm), int(beetle)
        )
        print(f"💾 [Database] 数据保存成功: T:{t} H:{h} P:{aphid+armyworm+beetle}")
    except Exception as e:
        # 如果这里还报 con/conn 错误，请检查 database/connect.py 里的函数实现
        print(f"❌ [Database Error] 无法存入数据: {e}")

def auto_recognition_task():
    """后台任务循环"""
    print("[System] 后台 AI 任务线程已启动...")
    # 给系统启动留一点缓冲时间
    time.sleep(5) 
    while True:
        try:
            execute_analysis_and_save()
        except Exception as e:
            print(f"⚠️ [Loop Error] 任务执行异常: {e}")
        time.sleep(15)

# 🚀 启动线程：确保只在主进程启动一次
if not any(t.name == "AI_Task" for t in threading.enumerate()):
    task_thread = threading.Thread(target=auto_recognition_task, name="AI_Task", daemon=True)
    task_thread.start()

# --- 前端 API 接口 ---

@app.route('/chart')
def chart_data_api():
    """图表数据接口：返回最新的环境与害虫数据"""
    try:
        row = select_env_data()
        if row:
            # 严格按照前端 layout 对应的索引返回
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
    except Exception as e:
        print(f"❌ [API Error] 查询数据库失败: {e}")
        
    return jsonify({"status": "no_data", "msg": "等待首条数据写入..."}), 200