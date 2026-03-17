# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import numpy as np
import time

class DHT11:
    def __init__(self, pin=17):  # 根据你给的代码，引脚是17
        self.pin = pin
        GPIO.setmode(GPIO.BCM)

    def read(self):
        """读取并返回温湿度字典"""
        # 1. 发送开始信号
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(self.pin, GPIO.HIGH)
        
        GPIO.setup(self.pin, GPIO.IN)

        # 2. 等待响应
        timeout = 0
        while GPIO.input(self.pin) == GPIO.LOW:
            timeout += 1
            if timeout > 1000: return {"error": "Sensor timeout"}
            continue

        while GPIO.input(self.pin) == GPIO.HIGH:
            continue

        # 3. 接收 40 位数据
        j = 0
        data = []
        while j < 40:
            k = 0
            while GPIO.input(self.pin) == GPIO.LOW:
                continue
            while GPIO.input(self.pin) == GPIO.HIGH:
                k += 1
                if k > 100: break
            
            if k < 8:
                data.append(0)
            else:
                data.append(1)
            j += 1

        # 4. 数据解析（使用你原来的 numpy 逻辑）
        m = np.logspace(7, 0, 8, base=2, dtype=int)
        data_array = np.array(data)
        
        try:
            humidity = m.dot(data_array[0:8])
            humidity_point = m.dot(data_array[8:16])
            temperature = m.dot(data_array[16:24])
            temperature_point = m.dot(data_array[24:32])
            check = m.dot(data_array[32:40])

            if check == (humidity + humidity_point + temperature + temperature_point):
                return {
                    "humidity": humidity,
                    "temperature": temperature,
                    "status": "success"
                }
            else:
                return {"error": "Checksum failed", "status": "error"}
        except Exception as e:
            return {"error": str(e), "status": "error"}

    def cleanup(self):
        GPIO.cleanup()
