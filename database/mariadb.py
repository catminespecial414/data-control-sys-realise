#弃用
# database/mariadb.py
# SQLite数据库模块

import pymysql
import datetime
from database import db

cursor = db.cursor()

temperature = 25.4
humidity = 60
pressure = 1013

sql = """
INSERT INTO env_data (temperature, humidity, pressure)
VALUES (%s,%s,%s)
"""

cursor.execute(sql,(temperature,humidity,pressure))

db.commit()
db.close()