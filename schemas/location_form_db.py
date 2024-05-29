from database_connection import get_db_connection

def initialize_database_location():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS smartHireIn")
        cursor.execute("USE smartHireIn")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS location_form (
            id INT AUTO_INCREMENT PRIMARY KEY,
            location_name VARCHAR(255) NOT NULL UNIQUE,
            city VARCHAR(255) NOT NULL,
            state VARCHAR(255) NOT NULL,
            zip_code VARCHAR(10) NOT NULL,
            time_zone VARCHAR(50) NOT NULL,
            country VARCHAR(255) NOT NULL
        )
        """)
        connection.commit()
    finally:
        cursor.close()
        connection.close()

