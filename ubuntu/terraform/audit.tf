resource "vault_audit" "vault_audit_file" {
  type = "file"

  options = {
    file_path = "/tmp/vault_audit.txt"

  }
}

resource "vault_generic_endpoint" "rate_limit_audit_logging" {
  path = "sys/quotas/config"

  data_json = jsonencode({
    enable_rate_limit_audit_logging = true
  })

  depends_on = [vault_audit.vault_audit_file]
}
