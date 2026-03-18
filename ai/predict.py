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
        
        # 你的目标过滤词（百度通用识别返回的是 keyword）
        self.target_pests = ["瓢虫", "螳螂", "天牛", "蚜虫", "甲虫"]

    def analyze(self):
        """抓拍、保存、识别并标注图片"""
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("无法打开摄像头")
            return []

        # 1. 转换成百度需要的格式
        _, img_encode = cv2.imencode('.jpg', frame)
        img_data = img_encode.tobytes()

        # 2. 调用百度通用物体识别接口
        # 注意：这里改成了 advancedGeneral 以匹配你后面的 keyword 逻辑
        result = self.client.advancedGeneral(img_data)
        
        found_pests = []
        
        # 3. 解析结果并在图片上写字
        if 'result' in result:
            items = result['result']
            for i, item in enumerate(items):
                name = item.get('keyword') # 通用识别用的是 keyword
                score = item.get('score')
                
                # 如果这个东西在你的目标名单里
                if name in self.target_pests:
                    found_pests.append(name)
                    # 在图片左上角画出检测到的名字（由于OpenCV画中文麻烦，我们印控制台，图上画序号）
                    cv2.putText(frame, f"Found: {name}", (10, 30 + i*30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            print(f"🔍 AI 识别结果: {found_pests}")
        else:
            print("⚠️ 百度 API 未返回结果:", result)

        # 4. 保存这张“证据图”到项目的 static 文件夹
        # 这样你在浏览器输入 http://IP:5000/static/last_ai.jpg 就能看到了
        save_path = os.path.join(os.path.dirname(__file__), "../static/last_ai.jpg")
        cv2.imwrite(save_path, frame)
        
        if not found_pests:
            print("✅ 画面正常，未发现目标害虫。")
            
        return found_pests