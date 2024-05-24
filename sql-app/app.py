from vault import read_vault_dbsecretAPI, read_vault_dbsecret, read_vault_kvv1
import pyodbc
import os
import time

def connect_sql(USERNAME, PASSWORD, SERVER, DATABASE):
    print("Connecting to database with credentials:")
    print(f"Database Server {SERVER}:{DATABASE}")
    print(f"Username: {USERNAME} - Password: {PASSWORD}")

    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};DATABASE={DATABASE};SERVER={SERVER};UID={USERNAME};PWD={PASSWORD};Encrypt=no'
    print(f"Connection String: {connectionString}")
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    SQL_QUERY = "SELECT * FROM location"
    print(f"Running query: {SQL_QUERY}")
    cursor.execute(SQL_QUERY)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    print("Closing connection to database")
    cursor.close()
    conn.close()

print("Waiting for demo to initialize...")
time.sleep(30)
while True:
    roleName = "mssql-role"
    print("Requesting database credentials from Vault")
    creds = read_vault_dbsecret(roleName)
    print("Requesting DB Server and Database name from Vault")
    dbInfo = read_vault_kvv1("BusinessUnit1", "sql-app/dev/dbinfo")
    print(f"DB info: Server {dbInfo['data']['db_server']} Database Name: {dbInfo['data']['db_database']}")

    print("######### Connection #############")
    try:
        resp1 = connect_sql(creds['data']['username'], creds['data']['password'], dbInfo['data']['db_server'], dbInfo['data']['db_database'])
    except pyodbc.InterfaceError as e:
        print(f"Failed to connect to database: {str(e)}")
        creds = read_vault_dbsecret(roleName)
        resp1 = connect_sql(creds['data']['username'], creds['data']['password'], dbInfo['data']['db_server'], dbInfo['data']['db_database'])
    print(resp1)
    time.sleep(5) 