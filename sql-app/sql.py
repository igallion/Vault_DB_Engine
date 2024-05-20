import pyodbc
import os
import time

SERVER = os.getenv('DB_SERVER')
DATABASE = os.getenv('DB_DATABASE')
USERNAME = os.getenv('DB_SA_USER')
PASSWORD = os.getenv('DB_SA_PASSWORD')

connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};DATABASE={DATABASE};SERVER={SERVER};UID={USERNAME};PWD={PASSWORD};Encrypt=no'
#Populate test data
conn = pyodbc.connect(connectionString)
cursor = conn.cursor()

sql_script = """
USE [Test_database];

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'location' AND type = 'U')
BEGIN
    CREATE TABLE location
    (
        street VARCHAR(20),
        city VARCHAR(20),
        state VARCHAR(20)
    );
    INSERT INTO location (street, city, state)
    VALUES
        ('main', 'anytown', 'california'),
        ('Cleveland RD', 'Wooster', 'Ohio');
END;
"""
cursor.execute(sql_script)
conn.commit()

cursor.close()
conn.close()

conn = pyodbc.connect(connectionString)
cursor = conn.cursor()
SQL_QUERY = "SELECT * FROM location"
cursor.execute(SQL_QUERY)
rows = cursor.fetchall()

for row in rows:
   print(row)

cursor.close()
conn.close()

print("Sleeping until cancelled...")
"""
while True:
   time.sleep(10)
"""