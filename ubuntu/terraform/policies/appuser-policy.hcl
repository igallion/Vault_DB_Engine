# Read and list keys under database/app1/ secrets engine 
path "database/app1/*" {
  capabilities = ["read", "list"]
}