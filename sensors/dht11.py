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
        """抗干扰增强版：针对 AI 高负载环境优化"""
        # 1. 触发传感器
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.1) # 稳定电平
        
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.02) # 关键：持续 20ms 的低电平触发信号
        
        # 2. 极其迅速地切换到输入模式并开启上拉
        GPIO.output(self.pin, GPIO.HIGH)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # 3. 等待传感器的响应信号（握手阶段）
        # 正常响应应该是：高 -> 低(80us) -> 高(80us)
        timeout = 0
        while GPIO.input(self.pin) == GPIO.HIGH:
            timeout += 1
            if timeout > 1000: return {"status": "error", "error": "No Response"}
        
        timeout = 0
        while GPIO.input(self.pin) == GPIO.LOW:
            timeout += 1
            if timeout > 1000: continue # 等待低电平结束

        timeout = 0
        while GPIO.input(self.pin) == GPIO.HIGH:
            timeout += 1
            if timeout > 1000: continue # 等待高电平结束

        # 4. 读取 40 位数据流
        raw_counts = []
        for j in range(40):
            # 等待低电平（起始位）结束
            while GPIO.input(self.pin) == GPIO.LOW:
                continue
            
            # 测量高电平持续时间
            k = 0
            while GPIO.input(self.pin) == GPIO.HIGH:
                k += 1
                if k > 2000: break
            raw_counts.append(k)

        # --- 打印诊断信息，如果还是失败，请看这里的数字 ---
        # print(f"🔍 [Debug] 序列: {raw_counts}")

        # 5. 解析数据 (基于你 test_dht.py 的反馈，暂定阈值为 10)
        # 如果 Checksum Failed，观察 raw_counts，将阈值设在“大数”和“小数”之间
        data = [1 if x > 10 else 0 for x in raw_counts]
        
        try:
            m = np.logspace(7, 0, 8, base=2, dtype=int)
            h_int = m.dot(data[0:8])
            h_dec = m.dot(data[8:16])
            t_int = m.dot(data[16:24])
            t_dec = m.dot(data[24:32])
            check = m.dot(data[32:40])

            # 校验和逻辑
            if check == (h_int + h_dec + t_int + t_dec) & 0xFF:
                return {
                    "humidity": float(f"{h_int}.{h_dec}"),
                    "temperature": float(f"{t_int}.{t_dec}"),
                    "status": "success"
                }
            else:
                return {"status": "error", "error": "Checksum Failed"}
        except Exception as e:
            return {"status": "error", "error": f"Parse Error: {str(e)}"}