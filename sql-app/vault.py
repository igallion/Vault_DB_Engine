import subprocess
import os
import json
import requests


def read_vault_dbsecret(role_name):
    # Assuming the environment variables are set in your system
    VAULT_TOKEN = os.getenv('VAULT_TOKEN')
    VAULT_ADDR = os.getenv('VAULT_ADDR')

    # Set environment for the subprocess
    env = os.environ.copy()
    env['VAULT_TOKEN'] = VAULT_TOKEN
    env['VAULT_ADDR'] = VAULT_ADDR

    endpoint = "database/creds/" + role_name
    # Vault command to execute
    command = ["vault", "read", "-format=json", endpoint]

    # Execute the command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        # Parse JSON output
        temp_creds = json.loads(result.stdout)
        return temp_creds
    except subprocess.CalledProcessError as e:
        print("Failed to execute command:", e)
        print(e.stderr)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)

def read_vault_dbsecretAPI(role_name):
    VAULT_TOKEN = os.getenv('VAULT_TOKEN')
    VAULT_ADDR = os.getenv('VAULT_ADDR')
    
    headers = {
    "X-Vault-Token": VAULT_TOKEN
    }

    url = f"{VAULT_ADDR}/v1/database/creds/" + role_name

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("success")
        temp_creds = response.json()
        return temp_creds

