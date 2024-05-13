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
    connection_url          = "sqlserver://{{username}}:{{password}}@localhost/mssql_vault_server_demo:1433/Test_database?TrustServerCertificate=True"
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
    "CREATE LOGIN [{{name}}] WITH PASSWORD = '{{password}}';",
    "CREATE USER [{{name}}] FOR LOGIN [{{name}}];",
    "GRANT SELECT ON SCHEMA::dbo TO [{{name}}];"
  ]
  #1 hour
  default_ttl = 3600
  #1 day
  max_ttl = 86400
}
