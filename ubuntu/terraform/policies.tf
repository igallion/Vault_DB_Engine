#---------------------
# Create policies
#---------------------

resource "vault_policy" "appuser-dev-policy" {
  name   = "sql-app-dev-appuser-policy"
  policy = file("policies/sql-app-dev-appuser-policy.hcl")
}

resource "vault_policy" "appuser-qa-policy" {
  name   = "ig-mypy-qa-policy"
  policy = file("policies/ig-mypy-qa-policy.hcl")
}

resource "vault_policy" "appuser-prod-policy" {
  name   = "ig-mypy-prod-policy"
  policy = file("policies/ig-mypy-prod-policy.hcl")
}

resource "vault_policy" "admin-policy" {
  name   = "admin-policy"
  policy = file("policies/admin-policy.hcl")
}

resource "vault_password_policy" "pyDB-password-policy" {
  name   = "pyDB-password-policy"
  policy = file("policies/pyDB-password-policy.hcl")
}
