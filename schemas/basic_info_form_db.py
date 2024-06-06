from database_connection import get_postgresql_connection

def initialize_database_basic():
    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS basic_info_form (
            id SERIAL PRIMARY KEY,
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
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()