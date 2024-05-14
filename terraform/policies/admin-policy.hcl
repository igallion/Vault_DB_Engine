# Define the policy
path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "auth/token/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "sys/policies/acl/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "sys/auth/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "sys/mounts/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "sys/capabilities" {
  capabilities = ["create", "read"]
}

path "sys/capabilities-self" {
  capabilities = ["create", "read"]
}

path "sys/config/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "sys/health" {
  capabilities = ["read", "sudo"]
}

path "sys/leases/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "sys/metrics" {
  capabilities = ["read"]
}

path "sys/raw/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "sys/replication/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "sys/revoke/*" {
  capabilities = ["update"]
}

path "sys/rotate" {
  capabilities = ["update"]
}

path "sys/seal" {
  capabilities = ["sudo"]
}

path "sys/unseal" {
  capabilities = ["sudo"]
}

path "sys/storage/optimize" {
  capabilities = ["sudo"]
}

path "sys/storage/prefix/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "sys/tools/hash" {
  capabilities = ["update"]
}

path "sys/tools/sign" {
  capabilities = ["create", "read", "update"]
}

path "sys/tools/verify" {
  capabilities = ["create", "read", "update"]
}

path "sys/expire/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Allow access to the UI and help endpoint
path "sys/ui/*" {
  capabilities = ["read", "list"]
}

path "sys/internal/ui/*" {
  capabilities = ["read", "list"]
}

path "sys/help/*" {
  capabilities = ["read"]
}
