import cx_Oracle

# Replace these variables with your database connection details
#sqlplus sqlplus sys/MyStrongPassword10@localhost:1521/FREEPDB1 as sysdba
username = 'sys'
password = 'MyStrongPassword10'
dsn = '192.168.0.237:1521/FREEPDB1'  # This is the Data Source Name or TNS (e.g., 'hostname:port/service_name')

try:
    # Establish the database connection
    connection = cx_Oracle.connect(username, password, dsn, mode=cx_Oracle.SYSDBA)
    print("Successfully connected to the database")

    # Create a cursor
    cursor = connection.cursor()

    # Execute a sample query
    cursor.execute("SELECT * FROM location")
    rows = cursor.fetchall()
    # Fetch and print the results
    print(rows)
    print("Listing location table")
    for row in rows:
        print(row)

except cx_Oracle.DatabaseError as e:
    print(f"Database connection error: {e}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
