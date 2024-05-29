from database_connection import get_db_connection

def initialize_database_registration():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS smartHireIn")
        cursor.execute("USE smartHireIn")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registration_form (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            mobile_number VARCHAR(20) NOT NULL,
            useremail VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            gender VARCHAR(10) NOT NULL
        )
        """)
        connection.commit()
    finally:
        cursor.close()
        connection.close()