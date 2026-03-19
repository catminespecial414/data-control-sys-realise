# -*- coding: utf-8 -*-
import os
import cv2
from aip import AipImageClassify

class Predict:
    def __init__(self):
        # 百度 API 凭证
        self.APP_ID = '7521003'
        self.API_KEY = '91SgkOuo9AU1D6lRmCjX9mtL'
        self.SECRET_KEY = 'dYa8S0oFYY19M8hF1TSzxUP35AOJsDGj'
        self.client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        
        # 目标过滤词
        self.target_pests = ["瓢虫", "螳螂", "天牛", "蚜虫", "甲虫", "昆虫", "粘虫"]

    def analyze(self, frame=None):
        """
        兼容模式：
        1. 视频流调用时传入 frame，实时识别。
        2. 定时任务调用时不传 frame，尝试读取最后一张实时图，确保数据连续。
        """
        try:
            # 如果没传 frame，尝试从 static 目录读最后一张实时图
            if frame is None:
                last_path = os.path.join(os.path.dirname(__file__), "../web/static/last_ai.jpg")
                if os.path.exists(last_path):
                    frame = cv2.imread(last_path)
                
            # 如果依然没有画面，直接返回空列表，防止后面 .count() 报错
            if frame is None:
                return []

            # 编码图片
            _, img_encode = cv2.imencode('.jpg', frame)
            img_data = img_encode.tobytes()

            # 调用百度 AI
            result = self.client.advancedGeneral(img_data)
            
            found_pests = []
            if 'result' in result:
                for i, item in enumerate(result['result']):
                    name = item.get('keyword')
                    # 检查是否在害虫名单中
                    if any(p in name for p in self.target_pests):
                        found_pests.append(name)
                        # 在图上画标注（仅用于演示）
                        cv2.putText(frame, f"AI: {name}", (20, 50 + i*40), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # 持续更新这张“证据图”
            save_path = os.path.join(os.path.dirname(__file__), "../web/static/last_ai.jpg")
            cv2.imwrite(save_path, frame)
            
            return found_pests # 确保返回的是 List

        except Exception as e:
            print(f"❌ Predict 模块异常: {e}")
            return []