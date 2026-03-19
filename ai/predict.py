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
        try:
            # ... 识别逻辑 ...
            found_pests = ["瓢虫"] # 举例
            return found_pests # 返回的是列表
        except Exception as e:
            print(f"AI Error: {e}")
            return [] # 【重要】失败时返回空列表，而不是 None