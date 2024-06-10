from database_connection import get_postgresql_connection

def initialize_department_table():
    try:
        with get_postgresql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS department (
                        id SERIAL PRIMARY KEY,
                        department_name VARCHAR(255) UNIQUE NOT NULL,
                        created_by VARCHAR(255) NOT NULL,
                        last_modified VARCHAR(10) NOT NULL
                    )
                """)
                connection.commit()
    except Exception as e:
        print(f"Error: {e}")