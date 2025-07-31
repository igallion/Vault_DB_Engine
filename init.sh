#!/bin/bash

# This script is used to initialize the Vault DB Engine environment.
DIR="compose/.secrets"
if [ ! -d "$DIR" ]; then
    mkdir $DIR
fi

echo 123 > $DIR/vault-token

# Build the my_ubuntu image
cd ubuntu
docker build -t my_ubuntu:latest .
cd ..