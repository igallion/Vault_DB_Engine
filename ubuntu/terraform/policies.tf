#---------------------
# Create policies
#---------------------

resource "vault_policy" "appuser-policy" {
  name   = "sql-app-appuser-policy"
  policy = file("policies/sql-app-appuser-policy.hcl")
}

resource "vault_policy" "admin-policy" {
  name   = "admin-policy"
  policy = file("policies/admin-policy.hcl")
}
