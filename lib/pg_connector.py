import psycopg2

def conn(user="autouser", password="autouser", host="192.168.0.6", port="5432", database="homeauto"):
    connection = psycopg2.connect(user = user,
                                password = password,
                                host = host,
                                port = port,
                                database = database)
    return connection


def insert_query(connection, query, data):
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
