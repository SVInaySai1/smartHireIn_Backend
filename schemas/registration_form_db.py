from psycopg2 import sql
from database_connection import get_postgresql_connection

def initialize_database_registration():
    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registration_form (
            id SERIAL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            country_code VARCHAR(5) NOT NULL,
            mobile_number VARCHAR(15) NOT NULL,
            useremail VARCHAR(255) NOT NULL PRIMARY KEY,
            password VARCHAR(255) NOT NULL,
            gender VARCHAR(10) NOT NULL
        )
        """)
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()