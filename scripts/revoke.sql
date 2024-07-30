USE [Test_database];
IF EXISTS (SELECT 1 FROM sys.database_principals WHERE name = '{{name}}')
BEGIN
    EXEC sp_droprolemember 'db_datareader', '{{name}}';
END
IF EXISTS (SELECT 1 FROM sys.database_principals WHERE name = '{{name}}')
BEGIN
    DROP USER [{{name}}];
END
IF EXISTS (SELECT 1 FROM sys.server_principals WHERE name = '{{name}}')
BEGIN
    DROP LOGIN [{{name}}];
END