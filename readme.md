# VAULT_DB_ENGINE
This project is intended to be a showcase of how HashiCorp Vault can be integrated into an environment as a platform for secrets and Public Key Infrastructure (PKI) management. The environment includes a Vault server running in dev mode, a RESTful API, a backend Microsoft SQL database, and a Prometheus server for metrics/monitoring. My SQL-APP project is referenced throughout this project, see here for more details: https://github.com/igallion/sql-app

## Features

- Secure dynamic secrets management using Vault’s Database Secrets Engine
- On-demand SSL certificate provisioning via Vault PKI
- Metrics exposure to Prometheus from both Vault and API
- Full environment orchestration with Docker Compose
- Terraform-based Vault configuration and role setup

## Getting Started:
If you haven't already, install Docker: https://docs.docker.com/get-started/get-docker/

Clone this repository: 
```shell
git clone https://github.com/igallion/Vault_DB_Engine.git
```

Navigate into the project directory:
```shell
cd Vault_DB_Engine
```

Run the init script:

*nix systems:
```shell
./init.sh
```

Windows:
```shell
.\init.ps1
```

Navigate into the compose directory and start it up:
```shell
cd compose

docker compose up
```

You can check on the status of the containers using:

```shell
docker compose ps

NAME                      IMAGE                                        COMMAND                  SERVICE      CREATED          STATUS                    PORTS
mssql_vault_server_demo   mcr.microsoft.com/mssql/server:2022-latest   "/opt/mssql/bin/laun…"   mssql        48 seconds ago   Up 47 seconds (healthy)   0.0.0.0:1433->1433/tcp, [::]:1433->1433/tcp, 0.0.0.0:1434->1434/udp, [::]:1434->1434/udp
my_ubuntu                 my_ubuntu:latest                             "/bin/bash -c /usr/l…"   myubuntu     47 seconds ago   Up 37 seconds             
prometheus                prom/prometheus                              "/bin/prometheus --c…"   prometheus   48 seconds ago   Up 47 seconds             0.0.0.0:9090->9090/tcp, [::]:9090->9090/tcp
sql-app                   ghcr.io/igallion/sql-app:main                "python main.py"         sqlapp       47 seconds ago   Up 26 seconds (healthy)   0.0.0.0:443->443/tcp, [::]:443->443/tcp
vault_server_demo         hashicorp/vault:1.20                         "vault server -dev -…"   vault        47 seconds ago   Up 37 seconds             0.0.0.0:8200->8200/tcp, [::]:8200->8200/tcp
```

Once all of the containers are running, make a request to the sql-app API:

```shell
curl -k https://localhost/sql-app

{"message":"[('main', 'anytown', 'california')]"}
```
**NOTE**: The -k option ignores certificate errors. Since the Vault server and its Certificate Authorities (CAs) are ephemeral, your machine will not trust the certificate presented by the API. This is safe to ignore in a test environment:

## How It's Made:

**Tech used:** HashiCorp Vault, Terraform, Microsoft SQL Server, Docker, Docker Compose

This project is a self contained environment with the following services:

1. **Vault**: A HashiCorp Vault server running in Dev mode. Stores application secrets and provides roles for dynamically generating database credentials. Also serves as a certificate authority (CA) and can generate certificates on demand.
2. **sqlapp**: A RESTful API application written using Python's FastAPI library. 
3. **mssql**: Serves as the backend database for sqlapp.
4. **prometheus**: Provides monitoring and metrics on Vault and sqlapp.
5. **my_ubuntu**: Initializes the MSSQL database with test data and applies the Vault configuration via Terraform. Typically Terraform configurations would be applied in a CI/CD pipeline and the state file would be located in secure storage. However for the purposes of this demo, a container within the project handles this.

### Vault

When **docker compose up** is run, the first service to start is mssql. Vault requires the database server to be up and available in order to create new users, and sqlapp depends on the database server to complete requests to its API. 

Once the database service is online and available, Vault is initialized. The my_ubuntu container first applies the configuration defined in the **ubuntu/terraform** directory. This includes configuring the kvv1 secrets engines for each business unit, auth methods, policies, the database secrets engine and its associated database roles. These will all be used by sqlapp to retrieve connection details and new database credentials. A root and intermediate CA are also configured and roles are set up to allow applications to request SSL certificates from Vault.

The Vault Web UI should now be available. Browse to http://localhost:8200 and log in with the root token **123**. Once there, you can browse the UI to view any secrets/roles you would like. For example, you can generate a new database user by browsing to **Secrets Engines** > **database** > **Roles** > **mssql-role**. Once there click **Generate credentials**, Vault will then return a new username and password:

![Credentials Generated by mssql-role](/images/vault/mssql-role-creds.png) Credentials Generated by mssql-role

After initialization is complete, my_ubuntu will list users from the Test_database every few seconds. You will notice unique users are created each time credentials are requested from Vault:

```shell
Listing users in database
Changed database context to 'Test_database'.
name                                                                                                                             create_date             modify_date            
-------------------------------------------------------------------------------------------------------------------------------- ----------------------- -----------------------
v-userpass-appuserdev-mssql-role-m0fXFfMjH3PyYCCUlWYc-1753802672                                                                 2025-07-29 15:24:32.547 2025-07-29 15:24:32.547

(1 rows affected)
```

### sqlapp

Finally, after the database is initialized and Vault has started, sqlapp starts up. However, you may notice permission denied errors in the sqlapp logs:
```shell
hvac.exceptions.Forbidden: permission denied, on post http://vault_server_demo:8200/v1/auth/userpass/login/appuserdev
```

This is because while Vault is up and available, the Terraform configuration has not been completed. The required auth methods, secrets engines, and roles do not yet exist. This is expected and the app will retry its connection to Vault until it is able to retrieve an SSL certificate, key, and database credentials from the mssql-role database role. 

This highlights one of the risks of tightly coupling an application with another service. Sqlapp is dependent upon Vault to retrieve a new set of database credentials on every request to the **/sql-app** endpoint. If Vault is not available, requests to the API will fail. Carefully considering when and how often you reach into Vault as well as ensuring Vault is highly available are both important factors in designing your Vault setup. Perhaps a more ideal setup would be to cache the database credentials and KV secrets for a longer period rather than making frequent requests for the same resource. 

After a few seconds the app should start successfully and will log any requests to the console:

```shell
docker logs sql-app

INFO:     192.168.65.1:62870 - "GET /sql-app HTTP/1.1" 200 OK
INFO:     192.168.65.1:42416 - "GET / HTTP/1.1" 200 OK
```

Sqlapp exposes two endpoints: 

**/** returns a simple hello world message:
```shell
{"Message":"Hello World"}
```
**/sql-app** returns the contents of the **location** table in the **Test_database** database using credentials generated by Vault:
```shell
{"message":"[('main', 'anytown', 'california')]"}
```

Each endpoint is defined in the sqlapp application. Requests are tracked for Prometheus metrics then the response is returned:
```Python
#Define api routes
@app.get("/")
def read_root():
    REQUEST_COUNTER.labels(endpoint="/").inc()
    logger.info("Returning message")
    return {"Message": "Hello World"}

@app.get("/sql-app", status_code=200)
def get_sql_app(response: Response):
    REQUEST_COUNTER.labels(endpoint='/sql-app').inc()
    resp = sql_app()
    logger.info(f"Returning response: {resp}")
    return {"message": f"{resp}"}
```

### Prometheus

Finally, coming back to monitoring and metrics; Prometheus does not have any dependencies on the other services so it will start up right away. Throughout this guide Prometheus has been collecting metrics on both Vault and sqlapp. Browse to http://localhost:9090 then click **Status** > **Target health** to view the configured monitors:

![prometheus targets](/images/prometheus/prometheus-targets.png)

We can query the metrics generated by sqlapp by browsing back to **Query** then searching for **app_requests_total**: 

![sqlapp metrics 1](/images/prometheus/sqlapp-metrics-1.png)

You can see that the total number of requests to the **/** endpoint are **2** and the total number of requests to **/sql-app** is **1**

Now, try generating more requests to both endpoints:

```shell
curl -k https://localhost/

curl -k https://localhost/sql-app
```

You should now see the total number of requests to each endpoint increase:

![sqlapp metrics 2](/images/prometheus/sqlapp-metrics-2.png)

Now, try running each command again 6 times:
```shell
for i in {1..6}; do curl -k https://localhost/; done

for i in {1..6}; do curl -k https://localhost/sql-app; done
```

The first command should return the same hello world message six times, then exit without an issue. However, you will notice an error when running the second command:

```shell
{"message":"[('main', 'anytown', 'california')]"}{"message":"[('main', 'anytown', 'california')]"}{"message":"[('main', 'anytown', 'california')]"}{"message":"[('main', 'anytown', 'california')]"}{"message":"[('main', 'anytown', 'california')]"}

Internal Server Error
```

We get the expected output the first five times, but the last one comes back with an error: **Internal Server Error**. This is due to the fact that rate limiting has been configured for the mssql-role database role in Vault:

```
resource "vault_quota_rate_limit" "db-rate-limit" {
  name           = "db-rate-limit"
  path           = "database/creds/mssql-role"
  rate           = 5
  interval       = 10
  block_interval = 30

  depends_on = [vault_database_secret_backend_role.mssql-role]
}
```
[secrets.tf](/ubuntu/terraform/secrets.tf)

Rate limits can be set on nearly any Vault API path, in this case database/creds/mssql-role. Clients are limited from making more than 5 requests in a 10 second interval. If the limit is exceeded, further requests are blocked for 30 seconds.

Protecting endpoints vulnerable to Denial of Service (DOS) attacks (either intentional or not) is crucial to protecting Vault and the MSSQL database in this case as well. Rate limits should also be considered on other endpoints such as auth roles. Doing so will help protect Vault from **lease explosions** where too many auth tokens are generated from login requests. These tokens are then persisted in the Vault database and in memory. This can degrade your Vault server's performance and greatly increase the memory and storage needed to run your server. 

We can also query Prometheus to view the number of rate limit violations being reported by Vault. In the query search bar enter:
```
vault_quota_rate_limit_violation
```

![vault rate limit violations](/images/prometheus/vault-metrics-rate-limit-violation.png)

## Cleanup
Open a new terminal and navigate to the Vault_DB_Engine/compose directory then run:
```shell
docker compose down
```

## Optimizations

1. Added healthchecks and dependencies in Docker compose to make sure Vault is up and available before sql-app starts
     * Replaces unreliable sleep period which would often require manual intervention
2. sql-app restarts until Vault is fully configured
     * This is needed since this entire environment is ephemeral. Vault is configured by the my_ubuntu container once it is up and available. Once complete sql-app can then access the resources it needs
3. Pull latest sql-app image from GH Packages rather than rebuilding locally

## Lessons Learned:

In making this project I've learned a great deal in orchestrating dependent services and taking advantage of Vault's secrets management features. Properly defining dependencies and health checks in my Docker Compose file, ensuring sqlapp doesn't crash on the first failed connection to Vault, and defining Vault's configuration as code all presented unique challenges as I worked through this project. 

## Closing notes:
You can find my LinkedIn here: https://www.linkedin.com/in/isaac-gallion/

The sql-app application referenced in this project is hosted in another repository here: https://github.com/igallion/sql-app