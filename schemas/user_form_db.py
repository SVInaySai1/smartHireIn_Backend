from database_connection import get_db_connection

def initialize_database_user_form():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS smartHireIn")
        cursor.execute("USE smartHireIn")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_form (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            department VARCHAR(255) NOT NULL,
            gender VARCHAR(50) NOT NULL,
            admin_access BOOLEAN NOT NULL,
            role VARCHAR(255) NOT NULL
        )
        """)
        connection.commit()
    finally:
        cursor.close()
        connection.close()
