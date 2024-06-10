from database_connection import get_postgresql_connection

def initialize_database_user_form():
    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_form (
            id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL UNIQUE,
            department VARCHAR(255) NOT NULL,
            gender VARCHAR(50) NOT NULL,
            admin_access BOOLEAN NOT NULL,
            role VARCHAR(255) NOT NULL
        )
        """)
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
