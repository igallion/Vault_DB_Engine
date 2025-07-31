# This script initializes the Vault DB Engine environment.
$dir = "compose/.secrets"
if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir | Out-Null
}

"123" | Set-Content "$dir/vault-token"

# Build the my_ubuntu image
Set-Location ubuntu
docker build -t my_ubuntu:latest .
Set-Location ..