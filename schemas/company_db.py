from database_connection import get_db_connection
def initialize_database_company():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS smartHireIn")
        cursor.execute("USE smartHireIn")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS company (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL UNIQUE,
            website_url VARCHAR(255) NOT NULL,
            phone_no VARCHAR(15) NOT NULL,
            industry_name VARCHAR(255) NOT NULL,
            image VARCHAR(255)  # Store the path to the image
        )
        """)
        connection.commit()
    finally:
        cursor.close()
        connection.close()
