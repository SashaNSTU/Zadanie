from src.config import host, user, password, db_name, port
import psycopg2

def update_db():

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM buildings;")

    except Exception as ex:
        print("[INFO] Error", ex)
    finally:
        if connection:
            connection.close()


def create_connection(host, port, user, password, db_name):
    connection = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True
    return connection
