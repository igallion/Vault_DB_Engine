import hvac.exceptions
import hvac
import json

VAULT_ADDR='http://192.168.0.237:8200/'
VAULT_TOKEN='123'


#team, appName, #env variables (lowercase and dehyphen)
#policy format: teamLower-appNameLower-envLower-policy
team = 'ig'.lower()
app_Name = 'Mypy'.lower().replace('-', '')
env = 'dev'.lower()

#DB info
username = 'sa'
password = 'MyStrongPassword10'
db_Server = '192.168.0.237'
db_Name = 'Test_database'
db_Type = 'mssql'
db_Info = {
    'mssql': {'plugin-name': 'mssql-database-plugin', 'connection-string': f'sqlserver://{{{{username}}}}:{{{{password}}}}@{db_Server}'},
    'oracle': {'plugin-name': 'vault-plugin-database-oracle', 'connection-string': f'{{{{username}}}}/{{{{password}}}}@{db_Server}:1521/{db_Name}'}
    }

#Vault info
mount_point = f'{app_Name}DB'
db_Engine_name = mount_point
db_Connection_name = f'{env}{db_Name}'
role_Name = f'{team}{env}{db_Name}'
policy_Name = f"{team}-{app_Name}-{env}-policy"
password_Policy = 'pyDB-password-policy'
username_Template = 'VLT_{{printf "%s_%s" (.RoleName) (random 20) | uppercase | truncate 26}}'

#Establish client connection to vault
client = hvac.Client(
    url=VAULT_ADDR,
    token=VAULT_TOKEN
)

if not client.is_authenticated():
    print("Client is not authenticated")
    raise hvac.exceptions.Unauthorized

#List DB engines
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

#Configure db connection
db_Connections = []
try:
    db_Connections = client.secrets.database.list_connections(mount_point=mount_point)
except hvac.exceptions.InvalidPath:
    pass

if not db_Connections or db_Connection_name not in db_Connections['data']['keys']:
    #Configure db connection
    print("Creating DB connection")
    client.secrets.database.configure(
        mount_point=mount_point,
        name=db_Connection_name,
        plugin_name=db_Info[db_Type]['plugin-name'],
        allowed_roles=role_Name,
        connection_url=db_Info[db_Type]['connection-string'],
        username_template=username_Template,
        password_policy=password_Policy,
        username=username,
        password=password
    )
elif db_Connection_name in db_Connections['data']['keys']:
    print("Connection already exists")

    connection_config = client.secrets.database.read_connection(
        name=db_Connection_name,
        mount_point=mount_point
    )

    allowed_roles = connection_config['data']['allowed_roles']

    if role_Name not in allowed_roles:
      print(f"Adding {role_Name} to allowed roles")
      allowed_roles.append(role_Name)

      client.secrets.database.configure(
          mount_point=mount_point,
          name=db_Connection_name,
          allowed_roles=allowed_roles,
          plugin_name=db_Info[db_Type]['plugin-name']
      )

    elif role_Name in allowed_roles:
       print(f"{role_Name} IS in allowed roles") 

#List database roles
role_list = []
try:
    role_list = client.secrets.database.list_roles(mount_point=mount_point)['data']
except hvac.exceptions.InvalidPath as e:
    pass

#Create role
if not role_list or role_Name not in role_list['keys']:
    print(f"Creating role {role_Name}")

    #Create db role
    with open('test.sql', 'r') as sql_file:
        creation_statements = (sql_file.read()).split('\n')

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
  capabilities = ["read"]
}}
'''

#Read existing policy from vault
policy = client.sys.read_policy(name=policy_Name)['data']['rules']

if pyDB_Policy not in policy:
    #Append db policy to existing policy, write back to vault
    policies = [policy, pyDB_Policy]
    new_Policy = "\n".join(policies)

    print("Updating Policy: ")
    print(new_Policy)

    client.sys.create_or_update_policy(
        name=policy_Name,
        policy=new_Policy
    )
else:
    print("DB policy already exists")

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
