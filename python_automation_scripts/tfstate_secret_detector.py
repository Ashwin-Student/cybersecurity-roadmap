import json
import argparse
from pathlib import Path

# Keys commonly containing sensitive plaintext data in state files
SENSITIVE_KEYS = {"password", "private_key", "secret_key", "api_token", "access_key", "connection_string"}

def audit_tfstate_secrets(tfstate_path: Path) -> None:
    """Inspect Terraform state JSON for unencrypted sensitive values."""
    print(f"[+] Auditing Terraform state file: {tfstate_path}\n")

    try:
        with open(tfstate_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        findings = 0
        resources = data.get("resources", [])

        print(f"{'Resource Type':<30} | {'Resource Name':<20} | {'Sensitive Attribute'}")
        print("-" * 75)

        for resource in resources:
            r_type = resource.get("type", "unknown")
            r_name = resource.get("name", "unnamed")

            for instance in resource.get("instances", []):
                attributes = instance.get("attributes", {})
                if not isinstance(attributes, dict):
                    continue

                for attr_key, attr_val in attributes.items():
                    if any(s_key in attr_key.lower() for s_key in SENSITIVE_KEYS):
                        if attr_val and isinstance(attr_val, str) and len(attr_val) > 3:
                            findings += 1
                            masked_val = attr_val[:2] + "*" * (len(attr_val) - 4) + attr_val[-2:] if len(attr_val) > 6 else "******"
                            print(f"{r_type:<30} | {r_name:<20} | {attr_key} ({masked_val})")

        print(f"\n[*] Terraform State Audit Complete. Flagged {findings} exposed sensitive attribute(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{tfstate_path}' not found.")
    except Exception as e:
        print(f"[-] State file audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Terraform state files for exposed plain-text credentials")
    parser.add_argument("-s", "--state", required=True, type=Path, help="Path to terraform.tfstate file")

    args = parser.parse_args()
    audit_tfstate_secrets(args.state)