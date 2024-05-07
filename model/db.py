# model/db.py
import mysql.connector # type: ignore

db_config = {
    "host": "159.65.128.24",
    "user": "thisisclinic",
    "password": "thisispassword",
    "database": "uic_clinic",
    "port": 3306,
}

def get_db():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        yield cursor, db
    finally:
        cursor.close()
        db.close()
