import os

import psycopg2


def context():
    try:
        db_host = os.getenv('DB_HOST', 'localhost')  # Default to 'localhost' if not set
        db_user = os.getenv('DB_USER', 'root')  # Default to 'root'

        db_password = os.getenv('DB_PASSWORD', '')  # Default to an empty string
        db_name = os.getenv('DB_NAME', 'mydatabase')
        db_port = os.getenv('DB_PORT', '5432')
        connection = psycopg2.connect(

            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )

        cursor = connection.cursor()
        return cursor, connection
    except Exception as e:
        print(f"An error occurred: {e}")


def execute_query(query):
    cursor, connection = context()
    if cursor is None or connection is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor.execute(query)
        connection.commit()  # Commit the transaction if needed
        print("Query executed successfully")
    except Exception as e:
        print(f"An error occurred while executing the query: {e}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection


def close_connection(cursor, connection):
    try:
        if cursor is not None:
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Error closing cursor: {e}")
