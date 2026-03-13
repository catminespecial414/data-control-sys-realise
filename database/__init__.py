# database/__init__.py
# 数据库模块初始化
import pymysql

db = pymysql.connect(
    host="localhost",
    user="root",
    password="你的密码",
    database="farm_iot"
)