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
        self.target_pests = ["瓢虫", "螳螂", "天牛", "蚜虫", "甲虫", "昆虫", "粘虫"]

    def analyze(self, frame=None):
        """兼容视频流(传frame)和定时任务(不传frame)"""
        try:
            # 如果没传 frame，尝试读最后一张实时图
            if frame is None:
                # 获取 static 目录的绝对路径
                base_dir = os.path.dirname(os.path.abspath(__file__))
                path = os.path.join(base_dir, "../web/static/last_ai.jpg")
                if os.path.exists(path):
                    frame = cv2.imread(path)
            
            if frame is None: return [] # 彻底没图则返回空列表

            # 百度 AI 识别
            _, img_encode = cv2.imencode('.jpg', frame)
            result = self.client.advancedGeneral(img_encode.tobytes())
            
            found_pests = []
            if 'result' in result:
                for i, item in enumerate(result['result']):
                    name = item.get('keyword')
                    if any(p in name for p in self.target_pests):
                        found_pests.append(name)
                        # 在图上标注
                        cv2.putText(frame, f"AI:{name}", (10, 30 + i*35), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # 保存实时图供前端展示
            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../web/static/last_ai.jpg")
            cv2.imwrite(save_path, frame)
            return found_pests
        except Exception as e:
            print(f"❌ AI 识别异常: {e}")
            return []