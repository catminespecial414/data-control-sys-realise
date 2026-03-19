# -*- coding: utf-8 -*-
import os
import cv2
from aip import AipImageClassify

class Predict:
    def __init__(self):
        self.APP_ID = '7521003'
        self.API_KEY = '91SgkOuo9AU1D6lRmCjX9mtL'
        self.SECRET_KEY = 'dYa8S0oFYY19M8hF1TSzxUP35AOJsDGj'
        self.client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.target_pests = ["瓢虫", "螳螂", "天牛", "蚜虫", "甲虫"]

    def analyze(self, frame):
        """
        被动接收来自视频流的帧，进行 AI 识别并存图
        """
        if frame is None: return []

        try:
            # 1. 编码
            _, img_encode = cv2.imencode('.jpg', frame)
            img_data = img_encode.tobytes()

            # 2. 百度识别
            result = self.client.advancedGeneral(img_data)
            
            found_pests = []
            if 'result' in result:
                for i, item in enumerate(result['result']):
                    name = item.get('keyword')
                    if any(p in name for p in self.target_pests):
                        found_pests.append(name)
                        # 在图上画红色框
                        cv2.putText(frame, f"AI: {name}", (20, 40 + i*40), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            
            # 3. 强制保存到 static 供网页图表和识别页显示
            # 注意路径要指向你 web/static 所在的真实位置
            save_path = os.path.join(os.path.dirname(__file__), "../web/static/last_ai.jpg")
            cv2.imwrite(save_path, frame)
            
            return found_pests
        except Exception as e:
            print(f"AI API Error: {e}")
            return []