from database import db

from database import db

def doSqlWork(statement, entity=None):
    cursor = db.cursor()

    try:
        cursor.execute(statement, entity)

        if statement.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
            return result

        db.commit()

    except Exception as e:
        print("SQL执行失败:", e)
        db.rollback()

    finally:
        cursor.close()