from database_connection import get_postgresql_connection

def initialize_database_company():
    connection = get_postgresql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS company (
            id SERIAL PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL UNIQUE,
            website_url VARCHAR(255) NOT NULL,
            phone_no VARCHAR(15) NOT NULL,
            industry_name VARCHAR(255) NOT NULL,
            image VARCHAR(255)  -- Store the path to the image
        )
        """)
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

