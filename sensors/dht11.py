# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import numpy as np
import time

class DHT11:
    def __init__(self, pin=17):
        self.pin = pin
        # 统一使用 BCM 编码 (GPIO 17 = Physical Pin 11)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def read(self):
        """读取并返回温湿度字典"""
        # 1. 发送开始信号
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(self.pin, GPIO.HIGH)
        
        GPIO.setup(self.pin, GPIO.IN)

        # 2. 等待响应（增加超时保护）
        timeout = 0
        while GPIO.input(self.pin) == GPIO.LOW:
            timeout += 1
            if timeout > 5000: return {"status": "error", "error": "timeout_low"}
        
        timeout = 0
        while GPIO.input(self.pin) == GPIO.HIGH:
            timeout += 1
            if timeout > 5000: return {"status": "error", "error": "timeout_high"}

        # 3. 接收 40 位数据
        data = []
        for j in range(40):
            k = 0
            while GPIO.input(self.pin) == GPIO.LOW:
                continue
            while GPIO.input(self.pin) == GPIO.HIGH:
                k += 1
                if k > 500: break
            
            if k < 15: # 这里的阈值根据树莓派 4B 性能微调
                data.append(0)
            else:
                data.append(1)

        # 4. 数据解析
        if len(data) < 40:
            return {"status": "error", "error": "data_incomplete"}

        m = np.logspace(7, 0, 8, base=2, dtype=int)
        data_array = np.array(data)
        
        try:
            humidity = m.dot(data_array[0:8])
            humidity_point = m.dot(data_array[8:16])
            temperature = m.dot(data_array[16:24])
            temperature_point = m.dot(data_array[24:32])
            check = m.dot(data_array[32:40])

            # 校验和检查
            if check == (humidity + humidity_point + temperature + temperature_point) % 256:
                return {
                    "humidity": float(f"{humidity}.{humidity_point}"),
                    "temperature": float(f"{temperature}.{temperature_point}"),
                    "status": "success"
                }
            else:
                return {"status": "error", "error": "checksum_failed"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def cleanup(self):
        GPIO.cleanup()