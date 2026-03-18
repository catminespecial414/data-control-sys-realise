# -*- coding: utf-8 -*-
#connect.py
from pymysql import Connection
from datetime import datetime
def init_db():
    global con
    con = Connection(
        host='10.33.134.226',
        port=3306,
        user='farm',
        database="farm_iot",
        password='123456'
    )
    cursor= con.cursor()

def select_env_data():
    cursor = con.cursor()
    sql = """
    SELECT temperature, humidity, soil, light, ph, aphid, armyworm, beetle
    FROM env_data
    ORDER BY collect_time DESC
    LIMIT 1
    """
    cursor.execute(sql)
    con.commit()
    return cursor.fetchone()

def insert_env_data(temperature, humidity,  soil, light, ph, aphid, armyworm, beetle):
    cursor = con.cursor()
    sql = """
        INSERT INTO env_data 
        (temperature, humidity, soil, light, ph, aphid, armyworm, beetle, collect_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    cursor.execute(sql, (temperature, humidity, soil, light, ph, aphid, armyworm, beetle))
    con.commit()

def select_user(id):
    cursor = con.cursor()
    sql = "SELECT id, password FROM users WHERE id = %s"
    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return {"userid": result[0], "password": result[1]}
    else:
        return None

def select_device():
    cursor = con.cursor()
    sql = "SELECT id, device_name, status, update_time FROM device_status"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    devices = []
    for row in result:
        devices.append({
            "id": row[0],
            "device_name": row[1],
            "status": int(row[2]),
            "update_time": row[3]
        })

    return devices

def alter_user(id, user_name, password):
    cursor = con.cursor()
    sql = """
        UPDATE users SET id = %s, name = %s, password = %s WHERE id = %s
        """
    result = cursor.execute(sql, (id, user_name, password, id))
    print(result)
    con.commit()
    cursor.close()