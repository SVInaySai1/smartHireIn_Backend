import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        port=3307,
        user="vinay",
        password="1234",
        database="smartHireIn",
        cursorclass=pymysql.cursors.DictCursor
    )
