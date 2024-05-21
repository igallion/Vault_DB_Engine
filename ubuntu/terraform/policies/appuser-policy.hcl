# Read and list keys under database/app1/ secrets engine 
path "database/creds/mssql-role" {
  capabilities = ["read", "list"]
}