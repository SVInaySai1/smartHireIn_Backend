from database_connection import get_postgresql_connection

def initialize_database_location():
    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS location_form (
            id SERIAL PRIMARY KEY,
            location_name VARCHAR(255) NOT NULL UNIQUE,
            city VARCHAR(255) NOT NULL,
            state VARCHAR(255) NOT NULL,
            zip_code VARCHAR(10) NOT NULL,
            time_zone VARCHAR(50) NOT NULL,
            country VARCHAR(255) NOT NULL
        )
        """)
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
