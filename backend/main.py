
from flask import Flask, jsonify
import time
from ai import Predict
from sensors import SensorManager
from .config import BAIDU_AI_CONF

from database.connect import insert_env_data, init_db

app = Flask(__name__)


try:
    init_db()
except Exception as e:
    print(f"数据库连接失败: {e}")


ai_engine = Predict()
sensor_engine = SensorManager()

@app.route('/api/all_data', methods=['GET'])
def get_data():
    """获取数据并同步至梁伟的数据库"""
    
    env = sensor_engine.get_all_data()
    temp = env.get("temperature", 0)
    humi = env.get("humidity", 0)
    
    pests = ai_engine.analyze() 
    
 
    c_aphid = pests.count('蚜虫')
    c_armyworm = pests.count('粘虫')

    c_beetle = pests.count('天牛') + pests.count('甲虫')


    try:
        
        insert_env_data(temp, humi, 0, 0, 0, c_aphid, c_armyworm, c_beetle)
        sync_status = "Sync Success"
    except Exception as e:
        sync_status = f"Sync Failed: {str(e)}"


    return jsonify({
        "temperature": temp,
        "humidity": humi,
        "pests": pests,
        "is_safe": len(pests) == 0,
        "db_sync": sync_status,
        "time": time.strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)