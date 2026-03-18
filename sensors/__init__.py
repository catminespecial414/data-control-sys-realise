# -*- coding: utf-8 -*-
from .dht11 import DHT11
import random

class SensorManager:
    def __init__(self):
        # 即使暂时不用，留着初始化也可以，只要不调用 read() 就不报错
        self.dht = DHT11(pin=17)

    def get_all_data(self):
        # --- 确保这个函数在 class 里面 (有缩进) ---
        # 暂时注释掉物理读取，避开 GPIO 权限报错
        # dht_res = self.dht.read() 
        
        temp = round(random.uniform(20, 30), 2)
        humi = round(random.uniform(40, 60), 2)
        
        res = {
            "temperature": temp,
            "humidity": humi,
            "soil": round(random.uniform(30, 70), 2),
            "light": random.randint(200, 800),
            "ph": 7.0
        }
        return res