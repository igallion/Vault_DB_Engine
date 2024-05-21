#----------------------------------------------------------
# Enable secrets engines
#----------------------------------------------------------

# Enable db secrets engine at database path
resource "vault_mount" "db" {
  path = "database"
  type = "database"
}

resource "vault_database_secret_backend_connection" "mssql" {
  backend           = vault_mount.db.path
  name              = "Test_database"
  verify_connection = true
  allowed_roles     = ["mssql-role"]

  mssql {
    connection_url          = "sqlserver://{{username}}:{{password}}@mssql_vault_server_demo"
    max_open_connections    = 5
    max_idle_connections    = 3
    max_connection_lifetime = 5

    username = "sa"
    password = "MyStrongPassword10"
  }
}

resource "vault_database_secret_backend_role" "mssql-role" {
  backend = vault_mount.db.path
  name    = "mssql-role"
  db_name = vault_database_secret_backend_connection.mssql.name

  creation_statements = [
    "USE [Test_database]",
    "CREATE LOGIN [{{name}}] WITH PASSWORD = '{{password}}';",
    "CREATE USER [{{name}}] FOR LOGIN [{{name}}];",
    "EXEC sp_addrolemember db_datareader, [{{name}}];"
  ]
  #90 Seconds
  default_ttl = 5
  #90 Seconds
  max_ttl = 10
}
