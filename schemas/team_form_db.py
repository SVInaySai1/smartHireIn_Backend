from database_connection import get_postgresql_connection

def initialize_database_team():
    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_form (
            id SERIAL,
            team_name VARCHAR(255) NOT NULL,
            no_of_members INTEGER NOT NULL,
            team_head VARCHAR(255) NOT NULL,
            name_of_members TEXT NOT NULL
        )
        """)
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
