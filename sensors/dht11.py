# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import numpy as np
import time
import os

class DHT11:
    def __init__(self, pin=17):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def read(self):
        """读取并返回温湿度字典 (针对高负载环境优化)"""
        # 尝试提升进程优先级（需要 sudo）
        try:
            os.nice(-15) 
        except:
            pass

        # 1. 发送开始信号
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.02) # 必须保证至少 18ms
        GPIO.output(self.pin, GPIO.HIGH)
        GPIO.setup(self.pin, GPIO.IN)

        # 2. 等待响应
        unchanged_count = 0
        while GPIO.input(self.pin) == GPIO.HIGH:
            unchanged_count += 1
            if unchanged_count > 5000: return {"status": "error", "error": "timeout_low"}
        
        unchanged_count = 0
        while GPIO.input(self.pin) == GPIO.LOW:
            unchanged_count += 1
            if unchanged_count > 5000: return {"status": "error", "error": "timeout_high"}

        # 3. 接收 40 位数据
        data = []
        for j in range(40):
            unchanged_count = 0
            while GPIO.input(self.pin) == GPIO.LOW:
                continue
            while GPIO.input(self.pin) == GPIO.HIGH:
                unchanged_count += 1
                if unchanged_count > 1000: break
            
          
            if unchanged_count < 8: 
                data.append(0)
            else:
                data.append(1)

        # 恢复优先级
        try:
            os.nice(0)
        except:
            pass

        if len(data) < 40:
            return {"status": "error", "error": "incomplete_data"}

        # 4. 数据解析
        m = np.logspace(7, 0, 8, base=2, dtype=int)
        data_array = np.array(data)
        
        try:
            h_int = m.dot(data_array[0:8])
            h_dec = m.dot(data_array[8:16])
            t_int = m.dot(data_array[16:24])
            t_dec = m.dot(data_array[24:32])
            check = m.dot(data_array[32:40])

            if check == (h_int + h_dec + t_int + t_dec) & 0xFF:
                return {
                    "humidity": float(f"{h_int}.{h_dec}"),
                    "temperature": float(f"{t_int}.{t_dec}"),
                    "status": "success"
                }
            else:
                return {"status": "error", "error": "checksum_failed"}
        except:
            return {"status": "error", "error": "parse_error"}