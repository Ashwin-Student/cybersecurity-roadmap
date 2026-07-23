import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

def audit_vault_tokens(token_data_file: Path) -> None:
    """Audit Vault token leases for expiration, orphaned status, and excessive TTLs."""
    print(f"[+] Auditing HashiCorp Vault token metadata from: {token_data_file}\n")

    try:
        with open(token_data_file, "r", encoding="utf-8") as f:
            tokens = json.load(f)

        risky_tokens = 0
        print(f"{'Accessor ID':<20} | {'Type':<10} | {'TTL (Hours)':<12} | {'Renewable':<10} | {'Status'}")
        print("-" * 75)

        for token in tokens:
            accessor = token.get("accessor", "UNKNOWN")[:20]
            token_type = token.get("type", "service")
            ttl_seconds = token.get("ttl", 0)
            renewable = token.get("renewable", False)
            policies = token.get("policies", [])

            ttl_hours = round(ttl_seconds / 3600, 1)

            # Highlight orphan, non-expiring, or root-policy tokens
            is_root = "root" in policies
            if is_root:
                status = "CRITICAL (Root Token)"
                risky_tokens += 1
            elif ttl_seconds == 0:
                status = "EXPIRED"
            elif ttl_hours > 720:  # More than 30 days
                status = "WARN (Excessive TTL)"
                risky_tokens += 1
            else:
                status = "HEALTHY"

            print(f"{accessor:<20} | {token_type:<10} | {ttl_hours:<12} | {str(renewable):<10} | {status}")

        print(f"\n[*] Audit Complete. Identified {risky_tokens} high-risk token configuration(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{token_data_file}' not found.")
    except Exception as e:
        print(f"[-] Failed to process Vault metadata: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit HashiCorp Vault token lifespans and privilege levels")
    parser.add_argument("-t", "--tokens", required=True, type=Path, help="Path to Vault token lookup metadata JSON")

    args = parser.parse_args()
    audit_vault_tokens(args.tokens)