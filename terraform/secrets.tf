#----------------------------------------------------------
# Enable secrets engines
#----------------------------------------------------------

# Enable db secrets engine at database path
resource "vault_mount" "db" {
  path = "database"
  type = "database"
}
