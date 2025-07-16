# Use an official Ubuntu base image
FROM ubuntu:latest

# Set environment variables to non-interactive (this prevents some prompts)
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update \
    && apt-get install -y gnupg software-properties-common curl iputils-ping telnet wget unzip jq \
    && curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc \
    && curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools18

RUN wget https://releases.hashicorp.com/vault/1.20.0/vault_1.20.0_linux_amd64.zip \
    && unzip -o vault_1.20.0_linux_amd64.zip -d /usr/local/bin/

RUN wget https://releases.hashicorp.com/terraform/1.8.3/terraform_1.8.3_linux_amd64.zip \
    && unzip -o terraform_1.8.3_linux_amd64.zip -d /usr/local/bin/

# Optional: Add SQLCMD to the PATH
ENV PATH="$PATH:/opt/mssql-tools18/bin"

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ubuntu_init /usr/local/bin/ubuntu_init/

COPY terraform/auth.tf terraform/main.tf terraform/policies.tf terraform/secrets.tf terraform/audit.tf terraform/pki.tf terraform/variables.tf /root/terraform/

COPY terraform/policies/ /root/terraform/policies
# Command to keep the container running (optional)
CMD ["tail", "-f", "/dev/null"]
