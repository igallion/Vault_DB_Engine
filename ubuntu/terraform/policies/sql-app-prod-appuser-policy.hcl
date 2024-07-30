# Read and list credentials under database/creds/mssql-role role 
path "database/creds/mssql-role" {
  capabilities = ["read", "list"]
}

#Read and list secrets
path "BusinessUnit1/sql-app/prod/*" {
  capabilities = ["read", "list"]
}