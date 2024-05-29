from database_connection import get_db_connection

def initialize_database_team():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS smartHireIn")
        cursor.execute("USE smartHireIn")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_form (
            id INT AUTO_INCREMENT PRIMARY KEY,
            team_name VARCHAR(255) NOT NULL UNIQUE,
            team_head VARCHAR(255) NOT NULL,
            no_of_members INT NOT NULL,
            name_of_member TEXT NOT NULL
        )
        """)
        connection.commit()
    finally:
        cursor.close()
        connection.close()