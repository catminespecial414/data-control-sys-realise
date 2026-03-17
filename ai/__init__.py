import cv2
import os
from aip import AipImageClassify


APP_ID = '7521003'
API_KEY = '91SgkOuo9AU1D6lRmCjX9mtL'
SECRET_KEY = 'dYa8S0oFYY19M8hF1TSzxUP35AOJsDGj'

client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

def get_prediction():
    
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return ["Error: Camera not found"]
    
    img_name = os.path.join(os.path.dirname(__file__), "temp.jpg")
    cv2.imwrite(img_name, frame)
    cap.release()

    with open(img_name, "rb") as f:
        img_data = f.read()

    result = client.advancedGeneral(img_data)
    

    if 'result' in result:
        keywords = [item['keyword'] for item in result['result']]
        return keywords
    return ["No objects detected"]