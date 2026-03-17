# -*- coding: utf-8 -*-
#connect.py
from pymysql import Connection

con = None
try:
    con = Connection(
        host='192.168.88.226',
        port=3306,
        user='farm',
        database="farm_iot",
        password='123456'
    )
    cursor = con.cursor()
    sql = "INSERT INTO env_data (humidity, temperature) VALUES (1.2 ,1.1)"
    cursor.execute(sql)
    print(cursor.execute("select * from env_data"))
    con.commit()
except Exception as e:
    print(e)
finally:

    print(type(con))
    con.close()