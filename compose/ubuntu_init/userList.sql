USE Test_database;
SELECT name, create_date, modify_date
FROM sys.database_principals
WHERE type_desc IN ('SQL_USER', 'WINDOWS_USER', 'WINDOWS_GROUP')
AND name LIKE 'v-token-mssql-role%';

