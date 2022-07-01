

import psycopg2
import pandas as pd

database = 'postgis'
user = 'read_user'
pwd = 'read_pwd'
host = 'liradb.postgres.database.azure.com'
port = 5432

query = """
SELECT * FROM altitude
WHERE way_id='28092984'
"""
args=None

def query_db(query, args=None):
    conn = psycopg2.connect(database=database, user=user, password=pwd, host=host, port=port) 
    cur = conn.cursor()
    data = pd.read_sql(query, conn, params=args, coerce_float=True)
    cur.close()
    conn.close()
    return data

data = query_db(query, args)
print(data)