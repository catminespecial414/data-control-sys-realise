# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import numpy as np
import time

class DHT11:
    def __init__(self, pin=17):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def read(self):
        """带有深度诊断功能的读取函数"""
        # 1. 信号初始化
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(self.pin, GPIO.HIGH)
        GPIO.setup(self.pin, GPIO.IN)

        # 2. 等待响应
        count = 0
        while GPIO.input(self.pin) == GPIO.HIGH:
            count += 1
            if count > 10000: return {"status": "error", "error": "No Response"}

        while GPIO.input(self.pin) == GPIO.LOW: continue
        while GPIO.input(self.pin) == GPIO.HIGH: continue

        # 3. 核心：抓取原始计数值
        raw_counts = []
        for j in range(40):
            while GPIO.input(self.pin) == GPIO.LOW: continue
            k = 0
            while GPIO.input(self.pin) == GPIO.HIGH:
                k += 1
                if k > 2000: break
            raw_counts.append(k)

        # --- 诊断输出：把这 40 个数打印出来 ---
        print(f"🔍 [Debug] 原始计数值序列: {raw_counts}")

        # 4. 尝试解析 (暂时用较松的阈值 10)
        data = [1 if x > 10 else 0 for x in raw_counts]
        
        m = np.logspace(7, 0, 8, base=2, dtype=int)
        try:
            h_int = m.dot(data[0:8])
            h_dec = m.dot(data[8:16])
            t_int = m.dot(data[16:24])
            t_dec = m.dot(data[24:32])
            check = m.dot(data[32:40])

            if check == (h_int + h_dec + t_int + t_dec) & 0xFF:
                return {"humidity": h_int, "temperature": t_int, "status": "success"}
            else:
                return {"status": "error", "error": "Checksum Failed"}
        except:
            return {"status": "error", "error": "Parse Error"}