#!/bin/bash
#export VAULT_ADDR='http://192.168.0.237:8200'
VAULT_UNSEAL_KEY=$(jq -r ".keys_base64[0]" "/run/secrets/VAULT_CLUSTER_INFO")
export VAULT_TOKEN=$(jq -r ".root_token" "/run/secrets/VAULT_CLUSTER_INFO")

SEALED=$(vault status -format=json | jq -r ".sealed")
echo "### Vault Sealed Status: '$SEALED' ###"

if [[ "$SEALED" == "true" ]]; then
    echo "Vault is sealed"
    # Uncomment the next line to perform unseal operation when you're sure all is correct
    vault operator unseal $VAULT_UNSEAL_KEY
    vault status
elif [[ "$SEALED" == "false" ]]; then
    echo "Vault is unsealed"
else
    echo "Unexpected value for SEALED: '$SEALED'"
fi
