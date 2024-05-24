import subprocess
import os
import json
import requests


def read_vault_dbsecret(role_name):
    # Assuming the environment variables are set in your system
    VAULT_ADDR = os.getenv('VAULT_ADDR')
    VAULT_USER = os.getenv('VAULT_USER')
    VAULT_PASS = os.getenv('VAULT_PASS')

    # Set environment for the subprocess
    env = os.environ.copy()
    env['VAULT_USER'] = VAULT_USER
    env['VAULT_PASS'] = VAULT_PASS
    env['VAULT_ADDR'] = VAULT_ADDR

    # Vault command to login with appuser credentials
    command = [f"vault", "login", "-format=json", "-method=userpass", f"username={VAULT_USER}", f"password={VAULT_PASS}"]
    
    print(f"Logging in to vault using userpass auth: {command}")

    # Execute the command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        # Parse JSON output
        vault_creds = json.loads(result.stdout)
        env['VAULT_TOKEN'] = vault_creds['auth']['client_token']
    except subprocess.CalledProcessError as e:
        print("Failed to execute command:", e)
        print(e.stderr)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)

    # Vault command to read db credentials
    endpoint = "database/creds/" + role_name
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

