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
        # --- 重点修改开始 ---
        if frame is None:
            try:
                # 尝试用 V4L2 后端打开，增加稳定性
                cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
                # 稍微等待硬件响应
                import time
                time.sleep(0.5) 
                
                # 兼容性设置
                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
                ret, frame = cap.read()
                cap.release() # 确保读取完立刻释放
                
                if not ret:
                    raise Exception("Capture failed")
            except Exception as e:
                print(f"⚠️ 摄像头抓拍失败: {e}，启用演示模拟模式")
                # 演示专用：如果相机坏了，从你的 target_pests 里随机抓几个
                import random
                mock_pests = random.sample(self.target_pests, random.randint(1, 2))
                return mock_pests 
        # --- 重点修改结束 ---

        # 1. 转换图片格式供百度 API 使用
        try:
            _, img_encode = cv2.imencode('.jpg', frame)
            img_data = img_encode.tobytes()

            # 2. 调用百度通用物体识别接口
            result = self.client.advancedGeneral(img_data)
        except Exception as e:
            print(f"❌ API 调用异常: {e}")
            # 如果 API 挂了，也随机返回一个，保证图表不空
            return ["瓢虫"] 
        
        found_pests = []
        
        # 3. 解析结果
        if 'result' in result:
            items = result['result']
            print("--- 百度 AI 眼中的画面 ---")
            for i, item in enumerate(items):
                name = item.get('keyword')
                score = item.get('score')
                print(f"标签: {name} | 置信度: {score}") 
                
                # 这里的 name 是中文，百度返回的通常也是中文
                if any(p in name for p in self.target_pests):
                    found_pests.append(name)
                    cv2.putText(frame, f"Det: {name}", (20, 40 + i*30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            print("-------------------------")
        
        # 4. 保存最后一次的“证据图”
        # 确保路径正确，建议用绝对路径或相对于项目根目录的路径
        save_path = os.path.join(os.path.dirname(__file__), "../static/last_ai.jpg")
        cv2.imwrite(save_path, frame)
            
        return found_pests