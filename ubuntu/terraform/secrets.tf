#----------------------------------------------------------
# Enable secrets engines
#----------------------------------------------------------

# Enable db secrets engine at database path
resource "vault_mount" "db" {
  path = "database"
  type = "database"
}

#KV-V1 store for Business Unit 1
resource "vault_mount" "kvv1-BU1" {
  path        = "BusinessUnit1"
  type        = "kv"
  options     = { version = "1" }
  description = "KVV1 secrets mount for Business Unit 1"
}

#DB information for sql-app
resource "vault_kv_secret" "secret-BU1" {
  path = "${vault_mount.kvv1-BU1.path}/sql-app/dev/dbinfo"
  data_json = jsonencode(
    {
      db_server   = "mssql_vault_server_demo",
      db_database = "Test_database"
    }
  )
}

#KV-V1 store for Business Unit 1
resource "vault_mount" "kvv1-BU2" {
  path        = "BusinessUnit2"
  type        = "kv"
  options     = { version = "1" }
  description = "KVV1 secrets mount for Business Unit 2"
}

#DB information for sql-app
resource "vault_kv_secret" "secret-BU2" {
  path = "${vault_mount.kvv1-BU2.path}/oracle-app/dev/dbinfo"
  data_json = jsonencode(
    {
      db_server   = "oracle_vault_server_demo",
      db_database = "Test_database"
    }
  )
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
    max_connection_lifetime = 10

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
