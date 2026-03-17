# -*- coding: utf-8 -*-
#connect.py
from pymysql import Connection
from datetime import datetime
def init_db():
    global con
    con = Connection(
        host='192.168.88.226',
        port=3306,
        user='farm',
        database="farm_iot",
        password='123456'
    )
    global cursor
    cursor= con.cursor()


def insert_env_data(temperature, humidity):

    sql = """
    INSERT INTO env_data
    (temperature, humidity, collect_time)
    VALUES (%s,%s,%s)
    """

    cursor.execute(sql, (
        temperature,
        humidity,
        datetime.now()
    ))
    con.commit()

def select_user(username, password):
    sql = """
    SELECT * FROM user
    WHERE username = %s AND password = %s
    """
    cursor.execute(sql, (
        username, password
    ))

def close_conn():
    cursor.close()