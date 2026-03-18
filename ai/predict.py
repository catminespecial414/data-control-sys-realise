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
        
        # 目标过滤词（可以根据百度返回的 keyword 自行添加）
        self.target_pests = ["瓢虫", "螳螂", "天牛", "蚜虫", "甲虫"]

    def analyze(self, frame=None):
        """
        识别逻辑：支持传入外部 frame 或 自动抓拍
        """
        # 如果外部没有传入 frame，则自己开启摄像头抓拍
        if frame is None:
            cap = cv2.VideoCapture(0)
            # 兼容性设置
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            ret, frame = cap.read()
            cap.release()
            if not ret:
                print("❌ 自动抓拍失败，请检查摄像头")
                return []

        # 1. 转换图片格式供百度 API 使用
        _, img_encode = cv2.imencode('.jpg', frame)
        img_data = img_encode.tobytes()

        # 2. 调用百度通用物体识别接口
        try:
            result = self.client.advancedGeneral(img_data)
        except Exception as e:
            print(f"❌ API 调用异常: {e}")
            return []
        
        found_pests = []
        
        # 3. 解析结果并在图片上实时标注
        if 'result' in result:
            items = result['result']
            print("--- 百度 AI 眼中的画面 ---")
            for i, item in enumerate(items):
                name = item.get('keyword')
                score = item.get('score')
                # 不管是不是害虫，全部打印出来看一眼
                print(f"标签: {name} | 置信度: {score}") 
                
                if name in self.target_pests:
                    found_pests.append(name)
                    cv2.putText(frame, f"Det: {name}", (20, 40 + i*30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            print("-------------------------")
        
        # 4. 无论是否识别到，都保存最后一次的“证据图”供浏览器查看
        save_path = os.path.join(os.path.dirname(__file__), "../static/last_ai.jpg")
        cv2.imwrite(save_path, frame)
            
        return found_pests