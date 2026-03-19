# -*- coding: utf-8 -*-
import os
import cv2
import time
import subprocess
from aip import AipImageClassify

class Predict:
    def __init__(self):
        # 百度 API 凭证
        self.APP_ID = '7521003'
        self.API_KEY = '91SgkOuo9AU1D6lRmCjX9mtL'
        self.SECRET_KEY = 'dYa8S0oFYY19M8hF1TSzxUP35AOJsDGj'
        self.client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        
        self.target_pests = ["瓢虫", "螳螂", "天牛", "蚜虫", "甲虫"]
        self.tmp_img = "/tmp/real_capture.jpg"

    def analyze(self, frame=None):
        """
        针对新版树莓派系统的真实识别逻辑
        """
        # 如果外部没有传入 frame (比如视频流没开)，我们手动抓拍一张真实的
        if frame is None:
            try:
                # 既然你能看到预览，说明 libcamera-still 绝对可用
                # -n: 不显示预览 | -o: 输出路径 | --immediate: 立即抓拍
                cmd = f"libcamera-still -n -o {self.tmp_img} --width 640 --height 480 --immediate"
                subprocess.run(cmd, shell=True, check=True, capture_output=True)
                
                frame = cv2.imread(self.tmp_img)
                if frame is None:
                    raise Exception("无法读取抓拍到的图像文件")
                print("✅ 成功抓取真实硬件画面")
            except Exception as e:
                print(f"❌ 抓拍失败: {e}")
                return ["硬件连接异常"]

        # --- 开始百度 AI 识别 ---
        try:
            _, img_encode = cv2.imencode('.jpg', frame)
            img_data = img_encode.tobytes()

            print("🧠 正在上传真实画面至百度云进行 AI 分析...")
            result = self.client.advancedGeneral(img_data)
            
            found_pests = []
            if 'result' in result:
                print("--- [真实 AI 识别报告] ---")
                for i, item in enumerate(result['result']):
                    name = item.get('keyword')
                    print(f"标签: {name}")
                    if any(p in name for p in self.target_pests):
                        found_pests.append(name)
                        # 在图上画出识别结果
                        cv2.putText(frame, f"Found: {name}", (30, 60 + i*40), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                print("-------------------------")
            
            # 保存识别后的证据图
            save_path = os.path.join(os.path.dirname(__file__), "../static/last_ai.jpg")
            cv2.imwrite(save_path, frame)
            
            return found_pests if found_pests else ["未发现害虫"]

        except Exception as e:
            print(f"❌ API 调用失败: {e}")
            return ["网络连接超时"]