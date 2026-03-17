# backend/scheduler.py
import time
from ai import Predict
from sensors import SensorManager

def auto_check_job():
    ai = Predict()
    sm = SensorManager()
    
    while True:
        print("\n--- 执行定时巡检 ---")
        # 1. 检测温湿度
        data = sm.get_all_data()
        print(f"当前环境: {data}")
        
        # 2. 检测害虫
        pests = ai.analyze()
        if pests:
            print(f"【报警】发现目标害虫: {pests}！准备触发控制模块...")
            # 这里以后可以调用 control 模块的函数，比如打开喷药装置
            
        # 3. 每隔 60 秒检测一次 (演示用，正式可改为 3600)
        time.sleep(60)

if __name__ == "__main__":
    auto_check_job()