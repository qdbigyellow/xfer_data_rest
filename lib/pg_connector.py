import psycopg2
import 

def conn():
    connection = psycopg2.connect(user = "autouser",
                                password = "autouser",
                                host = "192.168.0.6",
                                port = "5432",
                                database = "homeauto")
    return connection


def insert_query(connection, query, data):
    cursor = connection.cursor()
    cursor.execute(pg_insert_query, record_to_insert)
    connection.commit()
    cursor.close()

    



