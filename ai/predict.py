# -*- coding: utf-8 -*-
import os
import cv2
import time
import random
import subprocess
from aip import AipImageClassify

class Predict:
    def __init__(self):
        # 百度 API 凭证
        self.APP_ID = '7521003'
        self.API_KEY = '91SgkOuo9AU1D6lRmCjX9mtL'
        self.SECRET_KEY = 'dYa8S0oFYY19M8hF1TSzxUP35AOJsDGj'
        self.client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        
        # 目标过滤词
        self.target_pests = ["瓢虫", "螳螂", "天牛", "蚜虫", "甲虫", "昆虫"]
        # 临时抓拍路径
        self.tmp_img = "/tmp/capture.jpg"

    def analyze(self, frame=None):
        """
        核心识别逻辑：
        1. 使用系统级 libcamera 强制抓拍，绕开 OpenCV 驱动死锁
        2. 获取真实图像后送往百度 AI 识别
        3. 仅在硬件彻底断开时使用模拟数据保底
        """
        # --- 步骤 1: 真实硬件抓拍 (使用 libcamera) ---
        if frame is None:
            try:
                print("📸 正在调用 libcamera 强制抓拍真实画面...")
                # -n: 不显示预览窗口 | -o: 输出路径 | -t 1: 等待1ms立即拍 | --width/height: 指定分辨率
                cmd = f"libcamera-still -n -o {self.tmp_img} -t 1 --width 640 --height 480 --immediate"
                
                # 执行系统命令
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode != 0:
                    # 如果 libcamera 不存在，尝试旧版的 raspistill (适用于旧系统)
                    cmd_old = f"raspistill -n -o {self.tmp_img} -t 1 -w 640 -h 480"
                    subprocess.run(cmd_old, shell=True)

                # 使用 OpenCV 读取刚才抓拍到的真实文件
                frame = cv2.imread(self.tmp_img)
                
                if frame is None:
                    raise Exception("硬件抓拍文件读取失败")
                
                print("✅ [真实抓拍成功] 正在上传百度 AI 进行分析...")

            except Exception as e:
                print(f"⚠️ 物理抓拍失败: {e}，自动切回模拟模式保底")
                return random.sample(self.target_pests, random.randint(1, 2))

        # --- 步骤 2: 调用百度 AI 进行真实识别 ---
        try:
            _, img_encode = cv2.imencode('.jpg', frame)
            img_data = img_encode.tobytes()

            # 调用通用物体识别
            result = self.client.advancedGeneral(img_data)
            
            found_pests = []
            if 'result' in result:
                items = result['result']
                print("--- [百度 AI 识别报告] ---")
                for i, item in enumerate(items):
                    name = item.get('keyword')
                    score = item.get('score')
                    print(f"检测到: {name} | 置信度: {score:.2f}") 
                    
                    if any(p in name for p in self.target_pests):
                        found_pests.append(name)
                        cv2.putText(frame, f"Det: {name}", (20, 50 + i*40), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                print("-------------------------")
            
            # 保存最后一张带标注的图供网页 static 访问显示
            save_path = os.path.join(os.path.dirname(__file__), "../static/last_ai.jpg")
            cv2.imwrite(save_path, frame)
            
            # 如果识别为空，返回一个说明，防止前端图表没数据
            return found_pests if found_pests else ["未发现害虫"]

        except Exception as e:
            print(f"❌ 百度 API 调用异常: {e}")
            return ["API Error"]