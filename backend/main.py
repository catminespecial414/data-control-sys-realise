from database.connect import insert_env_data, init_db

init_db()
from flask import Flask, jsonify
from ai import Predict
from sensors import SensorManager
from .config import BAIDU_AI_CONF

app = Flask(__name__)


ai_engine = Predict()  
sensor_engine = SensorManager()

@app.route('/api/all_data', methods=['GET'])
def get_data():
    """获取传感器和AI的综合数据"""
    env = sensor_engine.get_all_data()
    pests = ai_engine.analyze()
    
    return jsonify({
        "temperature": env.get("temperature"),
        "humidity": env.get("humidity"),
        "pests": pests,
        "is_safe": len(pests) == 0,
        "time": env.get("status") 
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)