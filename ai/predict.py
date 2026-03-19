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
        
        # 目标过滤词
        self.target_pests = ["瓢虫", "螳螂", "天牛", "蚜虫", "甲虫", "昆虫"]
        self.tmp_img = "/tmp/ai_capture.jpg"

    def analyze(self, frame=None):
        """
        全自动兼容模式：
        1. 如果传入了 frame (来自视频流共享)，直接用。
        2. 如果 frame 为 None (来自 server.py 定时任务)，则尝试自动抓拍。
        """
        # --- 如果没传 frame，尝试从文件或硬件获取一次性抓拍 ---
        if frame is None:
            try:
                # 既然你的视频流在跑，libcamera 可能会 busy，
                # 我们尝试从你刚才保存的最新的 last_ai.jpg 里读，或者简单抓一张。
                # 这样可以完全避免参数缺失报错
                last_path = os.path.join(os.path.dirname(__file__), "../web/static/last_ai.jpg")
                if os.path.exists(last_path):
                    frame = cv2.imread(last_path)
                
                if frame is None:
                    # 如果连图都没有，只能跳过或返回空
                    return []
            except Exception as e:
                print(f"⚠️ 自动获取画面失败: {e}")
                return []

        # --- 核心识别逻辑 ---
        try:
            _, img_encode = cv2.imencode('.jpg', frame)
            img_data = img_encode.tobytes()

            # 调用百度识别
            result = self.client.advancedGeneral(img_data)
            
            found_pests = []
            if 'result' in result:
                for i, item in enumerate(result['result']):
                    name = item.get('keyword')
                    if any(p in name for p in self.target_pests):
                        found_pests.append(name)
                        # 在图上标注
                        cv2.putText(frame, f"AI: {name}", (20, 50 + i*40), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            
            # 保存证据图
            save_path = os.path.join(os.path.dirname(__file__), "../web/static/last_ai.jpg")
            cv2.imwrite(save_path, frame)
            
            return found_pests
        except Exception as e:
            print(f"❌ AI 接口异常: {e}")
            return []