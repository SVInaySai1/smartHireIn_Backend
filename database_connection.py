import psycopg2
from psycopg2.extras import DictCursor

def get_postgresql_connection():
    return psycopg2.connect(
        host="dpg-cpg4f2f79t8c73edkrh0-a.oregon-postgres.render.com",
        port=5432,
        user="smarthirein_user",
        password="MsPGHT9A1cpttHhlrplBJvcufpiCMfVc",  # Replace with your actual password
        database="smarthirein",
        cursor_factory=DictCursor
    )

# Example usage:
if __name__ == "__main__":
    try:
        connection = get_postgresql_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"PostgreSQL database version: {db_version}")
    except Exception as e:
        print(f"Error connecting to the PostgreSQL database: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
