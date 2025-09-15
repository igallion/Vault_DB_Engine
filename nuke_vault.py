import hvac
import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Default Vault config from environment
VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "123")
MAX_WORKERS = os.cpu_count() * 4


def create_client():
    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
    if not client.is_authenticated():
        raise Exception("Vault authentication failed.")
    return client


def create_token():
    client = create_client()
    try:
        client.auth.token.create(policies=["default"])
    except Exception:
        pass 


#Sends token creation requests in parallel. Used to demonstrate metrics in Prometheus/Grafana.
def main():
    parser = argparse.ArgumentParser(description="Create Vault tokens via API.")
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of tokens to create (default: 1)"
    )
    args = parser.parse_args()
    num_requests = args.count

    print(f"Creating {num_requests} Vault tokens...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_token) for _ in range(num_requests)]

        for i, future in enumerate(as_completed(futures), 1):
            if i % 100000 == 0:
                print(f"{i} tokens created...")

    print("Done.")


if __name__ == "__main__":
    main()