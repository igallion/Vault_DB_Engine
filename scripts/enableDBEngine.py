import hvac.exceptions
import hvac
import json

VAULT_ADDR='http://192.168.0.237:8200/'
VAULT_TOKEN='123'

mount_point = 'pyDB'
db_Connection_name = 'pythonDBConnection'
db_Engine_name = mount_point
db_Type = 'mssql-database-plugin'
role_Name = 'pyDBRole'
username = 'sa'
password = 'MyStrongPassword10'

client = hvac.Client(
    url=VAULT_ADDR,
    token=VAULT_TOKEN
    )

#Enable DB engine
secrets_engines_list = client.sys.list_mounted_secrets_engines()['data']
if f"{mount_point}/" not in secrets_engines_list.keys():
    print(f"Enabling secrets engine at: {mount_point}")

    #Enable db engine
    try:
        client.sys.enable_secrets_engine(
            backend_type='database',
            path=mount_point
        )
    except hvac.exceptions.InvalidRequest:
        pass
        #print("Path already in use")
else:
    print(f'Engine already enabled: {mount_point}')

#Create database role
role_list = []
try:
    role_list = client.secrets.database.list_roles(mount_point=mount_point)['data']
except hvac.exceptions.InvalidPath as e:
    pass

#Need to separate out db connection and role. Append role to allowed_roles instead of overwriting
if not role_list or role_Name not in role_list['keys']:
    print(f"Creating role {role_Name}")
    
    #Configure db connection
    client.secrets.database.configure(
        mount_point=mount_point,
        name=db_Connection_name,
        plugin_name=db_Type,
        allowed_roles=role_Name,
        connection_url=f'sqlserver://{{{{username}}}}:{{{{password}}}}@mssql_vault_server_demo',
        username=username,
        password=password
    )

    #Create db role
    with open('test.sql', 'r') as sql_file:
        creation_statements = (sql_file.read()).split('\n')
        print("Creation statements from file")
        print(creation_statements)

    client.secrets.database.create_role(
        name = role_Name,
        db_name = db_Connection_name,
        creation_statements=creation_statements,
        default_ttl='24h',
        max_ttl='48h',
        mount_point=db_Engine_name
    )
else:
    print(f'Role already exists: {role_Name}')

#Create DB role policy
policies = []
pyDB_Policy = f'''
#Read database creds
path "{db_Engine_name}/creds/{role_Name}" {{
  capabilities = ["read", "list"]
}}
'''

#Append to existing app policy
policy = client.sys.read_policy(name='py-policy')['data']['rules']
policies = [policy, pyDB_Policy]
new_Policy = "\n".join(policies)

print("New Policy: ")
print(new_Policy)

#List db connections
try:
    connections = client.secrets.database.list_connections(
        mount_point=mount_point
    )

    for connection in connections['data']['keys']:
        connectionConfig = client.secrets.database.read_connection(
            name=f'{connection}',
            mount_point=mount_point
        )

    print(connectionConfig['data'])
except hvac.exceptions.InvalidPath as e:
    print("DB connection does not exist")
    #print(e)
