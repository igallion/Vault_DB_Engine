# syntax=docker/dockerfile:1

FROM python:3.12.2-slim-bullseye

WORKDIR /sql-app

COPY requirements.txt /sql-app/

RUN apt-get update && \
    apt-get install -y curl gnupg python3-dev build-essential libpcre3 libpcre3-dev unixodbc unixodbc-dev g++ \
    && curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc \
    && curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

RUN pip3 install --no-cache -r requirements.txt

RUN wget https://releases.hashicorp.com/vault/1.16.2/vault_1.16.2_linux_amd64.zip \
    && unzip vault_1.16.2_linux_amd64.zip -d /usr/local/bin/

COPY app.py vault.py /sql-app/

CMD ["python3", "app.py"]
