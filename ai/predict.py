class Predict:
    def __init__(self):
        # ... (之前的初始化代码保持不变)
        self.APP_ID = '7521003'
        self.API_KEY = '91SgkOuo9AU1D6lRmCjX9mtL'
        self.SECRET_KEY = 'dYa8S0oFYY19M8hF1TSzxUP35AOJsDGj'
        self.client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        
      
        self.target_pests = ["瓢虫", "螳螂", "天牛"]

    def analyze(self):
        """抓拍并只过滤特定的害虫"""
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            return []

        img_path = os.path.join(os.path.dirname(__file__), "temp.jpg")
        cv2.imwrite(img_path, frame)

        with open(img_path, "rb") as f:
            img_data = f.read()

        # 调用百度接口获取所有识别到的物体
        result = self.client.advancedGeneral(img_data)
        all_keywords = [item['keyword'] for item in result.get('result', [])]

        # --- 核心过滤逻辑 ---
        # 只有当识别到的物体在我们的白名单里时，才保留它
        found_pests = [pest for pest in all_keywords if pest in self.target_pests]
        
        if found_pests:
            print(f"警报！检测到目标害虫: {found_pests}")
        else:
            print("画面正常，未发现目标害虫。")
            
        return found_pests