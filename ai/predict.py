# -*- coding: utf-8 -*-
import os
import cv2
import time
import random
import subprocess
from aip import AipImageClassify

class Predict:
    def __init__(self):
        self.APP_ID = '7521003'
        self.API_KEY = '91SgkOuo9AU1D6lRmCjX9mtL'
        self.SECRET_KEY = 'dYa8S0oFYY19M8hF1TSzxUP35AOJsDGj'
        self.client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.target_pests = ["瓢虫", "螳螂", "天牛", "蚜虫", "甲虫", "昆虫"]
        self.tmp_img = "/tmp/capture.jpg"

    def hardware_diagnostic(self):
        """硬件深度诊断：揪出病根"""
        print("\n🔍 --- 正在进行摄像头硬件体检 ---")
        
        # 1. 检查内核设备文件
        if os.path.exists("/dev/video0"):
            print("✅ 检查1: 系统已识别到 /dev/video0 设备文件。")
        else:
            print("❌ 检查1: 找不到 /dev/video0！可能是排线没插好或没开启 Legacy Camera。")

        # 2. 检查 vcgencmd (树莓派专用工具)
        try:
            res = subprocess.check_output("vcgencmd get_camera", shell=True, text=True)
            print(f"✅ 检查2: 树莓派底层状态 -> {res.strip()}")
            if "detected=0" in res:
                print("❗ 警告: 系统认到了接口，但没探测到摄像头(detected=0)。请重点检查排线！")
        except:
            print("⚠️ 检查2: 无法运行 vcgencmd，可能是非官方系统。")

        # 3. 检查是否有其他进程霸占
        try:
            lsof = subprocess.check_output("sudo lsof /dev/video0", shell=True, text=True)
            print(f"⚠️ 检查3: 发现摄像头被以下进程占用:\n{lsof}")
        except:
            print("✅ 检查3: 没有发现其他进程占用摄像头。")
        print("--------------------------------\n")

    def analyze(self, frame=None):
        if frame is None:
            # 每次尝试抓拍前先做一次体检
            self.hardware_diagnostic()
            
            try:
                print("📸 正在尝试通过系统命令抓拍...")
                # 尝试强制指定设备
                cmd = f"libcamera-still -n -o {self.tmp_img} -t 1 --immediate"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode != 0:
                    # 报错信息捕获
                    error_msg = result.stderr if result.stderr else "未知错误"
                    raise Exception(f"系统抓拍指令返回非零: {error_msg}")

                frame = cv2.imread(self.tmp_img)
                if frame is None:
                    raise Exception("抓拍文件生成了但无法读取(可能文件大小为0)")
                
                print("✅ [成功] 拿到真实画面！")

            except Exception as e:
                print(f"❌ 确定为硬件/驱动故障: {e}")
                print("💡 建议: 如果 'detected=0'，请关机重新插拔排线并确认蓝色面朝向网口。")
                return random.sample(self.target_pests, random.randint(1, 2))

        # 百度 AI 部分保持不变...
        try:
            _, img_encode = cv2.imencode('.jpg', frame)
            img_data = img_encode.tobytes()
            result = self.client.advancedGeneral(img_data)
            found_pests = []
            if 'result' in result:
                for i, item in enumerate(result['result']):
                    name = item.get('keyword')
                    if any(p in name for p in self.target_pests):
                        found_pests.append(name)
            
            save_path = os.path.join(os.path.dirname(__file__), "../static/last_ai.jpg")
            cv2.imwrite(save_path, frame)
            return found_pests if found_pests else ["未发现害虫"]
        except:
            return ["AI调用失败"]