from database_connection import get_db_connection

def initialize_database_profile():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS smartHireIn")
        cursor.execute("USE smartHireIn")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile_form (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email_id VARCHAR(255) NOT NULL UNIQUE,
            phone VARCHAR(15) NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL
        )
        """)
        connection.commit()
    finally:
        cursor.close()
        connection.close()
