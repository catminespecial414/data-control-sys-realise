# sensors/__init__.py
from .dht11 import DHT11
import random

class SensorManager:
    def __init__(self):
        # 确保引脚和硬件连接一致
        self.dht = DHT11(pin=17)

    # sensors/__init__.py

def get_all_data(self):
    # --- 暂时注释掉会导致报错的物理读取 ---
    # dht_res = self.dht.read() 
    
    # --- 改用模拟数据 (模拟 20-30度，40-60湿度) ---
    import random
    temp = round(random.uniform(20, 30), 2)
    humi = round(random.uniform(40, 60), 2)
    
    # 其他传感器如果也报 GPIO 错误，也可以同样注释掉改用随机数
    res = {
        "temperature": temp,
        "humidity": humi,
        "soil": round(random.uniform(30, 70), 2),
        "light": random.randint(200, 800),
        "ph": 7.0
    }
    return res