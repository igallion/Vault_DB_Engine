#--------------------------------
# Enable userpass auth method
#--------------------------------

resource "vault_auth_backend" "userpass" {
  type = "userpass"
}

# Create a user, 'appuserdev'
resource "vault_generic_endpoint" "appuserdev" {
  depends_on           = [vault_auth_backend.userpass]
  path                 = "auth/userpass/users/appuserdev"
  ignore_absent_fields = true

  data_json = <<EOT
{
  "policies": ["sql-app-dev-appuser-policy", "ig-mypy-dev-policy"],
  "password": "changeme"
}
EOT
}

# Create a user, 'appuserqa'
resource "vault_generic_endpoint" "appuserqa" {
  depends_on           = [vault_auth_backend.userpass]
  path                 = "auth/userpass/users/appuserqa"
  ignore_absent_fields = true

  data_json = <<EOT
{
  "policies": ["sql-app-qa-appuser-policy", "ig-mypy-qa-policy"],
  "password": "changeme"
}
EOT
}

# Create a user, 'appuserprod'
resource "vault_generic_endpoint" "appuserprod" {
  depends_on           = [vault_auth_backend.userpass]
  path                 = "auth/userpass/users/appuserprod"
  ignore_absent_fields = true

  data_json = <<EOT
{
  "policies": ["sql-app-prod-appuser-policy", "ig-mypy-prod-policy"],
  "password": "changeme"
}
EOT
}

# Create a user, 'admin'
resource "vault_generic_endpoint" "adminuser" {
  depends_on           = [vault_auth_backend.userpass]
  path                 = "auth/userpass/users/admin"
  ignore_absent_fields = true

  data_json = <<EOT
{
  "policies": ["admin-policy"],
  "password": "changeme"
}
EOT
}

resource "vault_auth_backend" "userpass2" {
  type        = "userpass"
  path        = "userpass2" # Optional; this is the default path
  description = "Userpass2 auth backend"
  tune {
    default_lease_ttl = "10s"
    max_lease_ttl     = "10s"
  }

}

# Create a user, 'appuserdev2'
resource "vault_generic_endpoint" "appuserdev2" {
  depends_on           = [vault_auth_backend.userpass2]
  path                 = "auth/userpass2/users/appuserdev2"
  ignore_absent_fields = true

  data_json = <<EOT
{
  "policies": ["sql-app-dev-appuser-policy", "ig-mypy-dev-policy"],
  "password": "changeme"
}
EOT
}
