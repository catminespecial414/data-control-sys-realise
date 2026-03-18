# sensors/__init__.py
from .dht11 import DHT11
import random

class SensorManager:
    def __init__(self):
        # 确保引脚和硬件连接一致
        self.dht = DHT11(pin=17)

    def get_all_data(self):
        """统一获取并整合所有传感器数据"""
        # 1. 尝试读取真实的 DHT11 温湿度
        dht_res = self.dht.read()
        
        # 2. 逻辑判断：如果读取成功则用真值，失败则给个默认值（演示用）
        if dht_res.get("status") == "success":
            temperature = float(dht_res.get("temperature", 0))
            humidity = float(dht_res.get("humidity", 0))
        else:
            # 如果没连硬件，为了让前端不显示 0，可以暂时给个模拟值，或者保持 0
            temperature = 0.0 
            humidity = 0.0

        # 3. 返回 server.py 需要的完整字典
        # 目前 soil, light, ph 没有硬件，直接在这里生成模拟数据
        return {
            "temperature": temperature,
            "humidity": humidity,
            "soil": round(random.uniform(30, 70), 2),  # 模拟土壤湿度
            "light": random.randint(200, 800),         # 模拟光照
            "ph": round(random.uniform(5.5, 7.5), 2)    # 模拟PH值
        }