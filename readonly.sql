USE [myapp];
CREATE LOGIN [{{name}}] WITH PASSWORD = '{{password}}';
CREATE USER [{{name}}] FOR LOGIN [{{name}}];
EXEC sp_addrolemember db_datareader, [{{name}}];
