from database_connection import get_db_connection

def initialize_database_basic():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS smartHireIn")
        cursor.execute("USE smartHireIn")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS basic_info_form (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_position VARCHAR(255) NOT NULL UNIQUE,
            job_category VARCHAR(255) NOT NULL,
            job_type VARCHAR(255) NOT NULL,
            department VARCHAR(255) NOT NULL,
            job_location VARCHAR(255) NOT NULL,
            hiring_type VARCHAR(255) NOT NULL,
            no_of_opening INT NOT NULL
        )
        """)
        connection.commit()
    finally:
        cursor.close()
        connection.close()
