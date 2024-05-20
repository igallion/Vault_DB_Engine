from vault import read_vault_dbsecretAPI, read_vault_dbsecret
import pyodbc
import os
import time

roleName = "mssql-role"
print("Requesting database credentials from Vault")
creds = read_vault_dbsecret(roleName)

def connect_sql(USERNAME, PASSWORD):
    SERVER = os.getenv('DB_SERVER')
    DATABASE = os.getenv('DB_DATABASE')
    #USERNAME = creds['data']['username']
    #PASSWORD = creds['data']['password']

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

print("######### Connection 1 #############")
try:
    resp1 = connect_sql(creds['data']['username'], creds['data']['password'])
except pyodbc.InterfaceError as e:
    print(f"Failed to connect to database: {str(e)}")
    creds = read_vault_dbsecret(roleName)
    resp1 = connect_sql(creds['data']['username'], creds['data']['password'])
time.sleep(2)
print(resp1)

print("######### Connection 2 #############")
try:
    resp2 = connect_sql(creds['data']['username'], creds['data']['password'])
except pyodbc.InterfaceError as e:
    print(f"Failed to connect to database: {str(e)}")
    creds = read_vault_dbsecret(roleName)
    resp2 = connect_sql(creds['data']['username'], creds['data']['password'])
time.sleep(6)
print(resp2)

print("######### Connection 3 #############")
try:
    resp3 = connect_sql(creds['data']['username'], creds['data']['password'])
except pyodbc.InterfaceError as e:
    print(f"Failed to connect to database: {str(e)}")
    creds = read_vault_dbsecret(roleName)
    resp3 = connect_sql(creds['data']['username'], creds['data']['password'])
time.sleep(6)
print(resp3)