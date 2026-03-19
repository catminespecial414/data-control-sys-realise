# -*- coding: utf-8 -*-
import time
import random
from .dht11 import DHT11

class SensorManager:
    def __init__(self):
        # 确认 DHT11 数据线接在 GPIO 17 (Pin 11)
        self.dht = DHT11(pin=17)

    def get_all_data(self):
        """核心方法：被后台任务调用，返回环境全数据"""
        temp, humi = 0, 0
        success = False
        
        for i in range(3):
            try:
                res = self.dht.read()
                if res.get("status") == "success":
                    temp = res["temperature"]
                    humi = res["humidity"]
                    success = True
                    print(f"[Sensor] 物理读取成功: Temp {temp}C, Humi {humi}%")
                    break
            except Exception as e:
                print(f"[Sensor] 第 {i+1} 次尝试失败: {e}")
            
            time.sleep(2.1) # DHT11 硬件要求两次读取间隔 > 2s

        if not success:
            print("[Sensor] 物理读取连续失败，使用模拟数据...")
            temp = round(random.uniform(22.0, 26.5), 1)
            humi = round(random.uniform(45.0, 55.0), 1)

        return {
            "temperature": temp,
            "humidity": humi,
            "soil": round(random.uniform(30, 60), 2),  # 模拟土壤湿度
            "light": random.randint(300, 700),         # 模拟光照
            "ph": round(random.uniform(6.5, 7.5), 2)   # 模拟PH值
        }