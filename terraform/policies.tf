#---------------------
# Create policies
#---------------------

# Create 'training' policy
resource "vault_policy" "appuser-policy" {
  name   = "appuser-policy"
  policy = file("policies/appuser-policy.hcl")
}

resource "vault_policy" "admin-policy" {
  name   = "admin-policy"
  policy = file("policies/admin-policy.hcl")
}
