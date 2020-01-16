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
    cursor.execute(pg_insert_query, record_to_insert)
    connection.commit()
    cursor.close()

    

async def a_conn():
    """
    Not finish. a connection for asyncio
    """

    connection = psycopg2.connect(user = "autouser",
                            password = "autouser",
                            host = "192.168.0.6",
                            port = "5432",
                            database = "homeauto")
    cursor = connection.cursor()

    pg_insert_query = """INSERT INTO public.financial_matrix ("symbol", "EPS_Growth", "FCF_Growth", "PB_Ratio", "PE_Ratio", "EBIT_Growth") VALUES (%s,%s,%s,%s,%s,%s)
       ON CONFLICT ("symbol")
       DO
          UPDATE 
          SET "EPS_Growth" = EXCLUDED."EPS_Growth",
          "FCF_Growth" = EXCLUDED."FCF_Growth",
          "PB_Ratio" = EXCLUDED."PB_Ratio",
          "PE_Ratio" = EXCLUDED."PE_Ratio",
          "EBIT_Growth" = EXCLUDED."EBIT_Growth";
    """
    record_to_insert = (symbol, eps_growth, fcf_growth, pb_ratio, pe_ratio, ebit_growth)
    cursor.execute(pg_insert_query, record_to_insert)
    connection.commit()
    cursor.close()
    connection.close()

