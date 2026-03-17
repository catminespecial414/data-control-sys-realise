# -*- coding: utf-8 -*-
from database import db

def execute(sql, params=None):
    global db
    cursor = db.cursor()
    if db is None:
        raise Exception("数据库未初始化！请先调用 init_db()")
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    cursor.commit()

    return cursor


def query(sql):
    cursor = db.cursor()
    cursor.execute(sql)

    result = cursor.fetchall()

    cursor.close()
    return result