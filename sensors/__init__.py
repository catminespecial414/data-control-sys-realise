# sensors/__init__.py
from .dht11 import DHT11

class SensorManager:
    def __init__(self):
        self.dht = DHT11(pin=17) # 确保引脚和你硬件连接一致

    def get_all_data(self):
        return self.dht.read()