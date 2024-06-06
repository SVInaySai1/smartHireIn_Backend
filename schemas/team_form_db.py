from database_connection import get_postgresql_connection

def initialize_database_team():
    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_form (
            id SERIAL PRIMARY KEY,
            team_name VARCHAR(255) NOT NULL UNIQUE,
            team_head VARCHAR(255) NOT NULL,
            no_of_members INT NOT NULL,
            name_of_member TEXT[] NOT NULL
        )
        """)
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
