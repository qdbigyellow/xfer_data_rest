import json
import urllib.request as request
import psycopg2

def fetch_data_to_gateway():
    for data in fetch_data():
        for loan in data:
            r = loan["rate"].replace("*&nbsp;", "").replace(",", ".")
            # print(r)
            af = loan["repaymentFreedomMax"]
            # if "*&nbsp;" in r:
            #    r = r.replace("*&nbsp;", "")
                # print(r)
            #if "," in r:
            #    r = r.replace(",", ".")
                # print(r)
            if float(r) < 100 and af.lower() == "nej":
                print(loan["loanPeriodMax"])
                print(r)

def fetch_data():
    result = json.load(request.urlopen("https://bank.nordea.dk/wemapp/api/credit/fixedrate/bonds.json"))
    yield result

if __name__  == '__main__':
    connection = psycopg2.connect(user = "autouser",
                                  password = "autouser",
                                  host = "192.168.0.6",
                                  port = "5432",
                                  database = "homeauto")
    cursor = connection.cursor()
    print ( connection.get_dsn_parameters(),"\n")
    print(cursor.execute("""
        SELECT *
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name   = 'financial_matrix';
    """))                                   
    pg_insert_query = """INSERT INTO public.financial_matrix ("symbol", "EPS_Growth", "FCF_Growth", "PB_Ratio", "PE_Ratio", "EBIT_Growth") VALUES (%s,%s,%s,%s,%s,%s);"""
    record_to_insert = ('fds', 0.0, 1.0, 2.0, 3.0, 4.0)
    cursor.execute(pg_insert_query, record_to_insert)
    connection.commit()
