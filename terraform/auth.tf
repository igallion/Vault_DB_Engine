#--------------------------------
# Enable userpass auth method
#--------------------------------

resource "vault_auth_backend" "userpass" {
  type = "userpass"
}

# Create a user, 'appuser'
resource "vault_generic_endpoint" "appuser" {
  depends_on           = [vault_auth_backend.userpass]
  path                 = "auth/userpass/users/appuser"
  ignore_absent_fields = true

  data_json = <<EOT
{
  "policies": ["appuser-policy"],
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


