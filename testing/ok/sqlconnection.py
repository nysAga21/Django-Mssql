import pyodbc
from decouple import config

def connect_to_sql_server():
    server = 'DESKTOP-QL5R938\SQLEXPRESS'
    database = 'Customer'
    username = 'sa'
    password = config('DB_PASSWORD')
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    return conn

def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


# print(execute_query(connect_to_sql_server(),'SELECT * FROM CustomerAccounts;'))