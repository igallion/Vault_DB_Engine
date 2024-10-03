resource "vault_audit" "vault_audit_file" {
  type = "file"

  options = {
    file_path = "/tmp/vault_audit.txt"
  }
}
