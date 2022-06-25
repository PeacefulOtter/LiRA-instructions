
from psycopg2.extras import execute_values

import pandas as pd
import psycopg2
import os

from dotenv import load_dotenv
load_dotenv()

user = os.getenv('username')
pwd = os.getenv('password')


def connect_db(database, user, pwd, host, port):
    print("\nConnecting to database")
    return psycopg2.connect(database=database, user=user, password=pwd, host=host, port=port) 
    
def disconnect_db(conn, cursor):
    if conn:
        cursor.close()
        conn.close()
        print("database connection is closed")

def query_db(callback):
    conn = connect_db('postgis', user, pwd, 'liradb.postgres.database.azure.com', 5432)
    cur = conn.cursor()
    res = callback(conn, cur)
    disconnect_db(conn, cur)
    return res

def select_db(query, args=None):
    def callback(conn, cur):
        return pd.read_sql(query, conn, params=args, coerce_float=True)
    return query_db(callback)

def insert_db(query, args):
    print('Inserting to PostGIS:\n\t -->', query)
    def callback(conn, cur):
        try:
            execute_values(cur, query, args)
            conn.commit()
        except:
            print("Duplicate keys, skipping segment")
    query_db(callback)

