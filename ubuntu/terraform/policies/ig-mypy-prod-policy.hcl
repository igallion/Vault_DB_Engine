#Read and list secrets
path "BusinessUnit1/sql-app/prod/*" {
  capabilities = ["read", "list"]
}