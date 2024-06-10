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

def delete_all_tables():
    try:
        connection = get_postgresql_connection()
        cursor = connection.cursor()

        # Get all table names in the schema
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = cursor.fetchall()

        # Drop each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')  # Use double quotes for table name
            print(f"Dropped table: {table_name}")

        connection.commit()
        print("All tables dropped successfully.")
    except Exception as e:
        connection.rollback()
        print(f"Error deleting tables: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Example usage:
if __name__ == "__main__":
    delete_all_tables()
