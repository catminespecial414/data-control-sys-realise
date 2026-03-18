import cv2
import time

class Camera:
    def capture(self, save_path="static/last_ai.jpg"):
        # 使用 CAP_V4L2 后端更稳定，防止 Busy 报错
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        
        # 给硬件一点启动时间
        time.sleep(1) 
        
        if not cap.isOpened():
            print("❌ 无法打开摄像头")
            return False

        ret, frame = cap.read()
        if ret:
            cv2.imwrite(save_path, frame)
            print(f"✅ 照片已保存至: {save_path}")
        
        # 核心：必须 release，否则下次刷新必报 Device Busy
        cap.release()
        return ret