#!/bin/bash
VAULT_UNSEAL_KEY=$(jq -r ".keys_base64[0]" "/run/secrets/VAULT_CLUSTER_INFO")
#export VAULT_TOKEN=$(jq -r ".root_token" "/run/secrets/VAULT_CLUSTER_INFO")

echo "Initializing Demo..."

SEALED=$(vault status -format=json | jq -r ".sealed")
echo "### Vault Sealed Status: '$SEALED' ###"

if [[ "$SEALED" == "true" ]]; then
    echo "Vault is sealed"
    vault operator unseal $VAULT_UNSEAL_KEY
    vault status
elif [[ "$SEALED" == "false" ]]; then
    echo "Vault is unsealed"
else
    echo "Unexpected value for SEALED: '$SEALED'"
fi

echo "Initializing Terraform"
cd /root/terraform
terraform init

echo "Configuring Vault"
terraform apply -auto-approve

echo "Initializing SQL database"
sqlcmd -C -U $SQL_USER -P $MSSQL_SA_PASSWORD -S mssql_vault_server_demo -i /usr/local/bin/ubuntu_init/configure.sql

#List users in database while demo is running
while true; do 
    echo "Listing users in database"
    sqlcmd -C -U $SQL_USER -P $MSSQL_SA_PASSWORD -S mssql_vault_server_demo -i /usr/local/bin/ubuntu_init/userList.sql
    sleep 5
done
