# -*- coding: utf-8 -*-
# database/__init__.py
# 数据库模块初始化
from pymysql import Connection
db = None
def init_db():
    global db
    if db is None:
        db = Connection(
            host="192.168.88.226",
            port=3306,
            user="farm",
            password="123456",
            database="farm_iot",
        )
        print("MariaDB connected")
    return db
