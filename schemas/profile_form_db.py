from database_connection import get_postgresql_connection

def initialize_database_profile():
    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile_form (
            id SERIAL PRIMARY KEY,
            email_id VARCHAR(255) NOT NULL UNIQUE,
            phone VARCHAR(15) NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL
        )
        """)
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
