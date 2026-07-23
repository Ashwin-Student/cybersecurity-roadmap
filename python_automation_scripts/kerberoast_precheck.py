import json
import argparse
from pathlib import Path

def audit_spn_accounts(json_input: Path) -> None:
    """Parse active directory user exports and identify high-risk Kerberoastable SPN accounts."""
    print(f"[+] Importing Active Directory user dataset from: {json_input}\n")

    try:
        with open(json_input, "r", encoding="utf-8") as f:
            accounts = json.load(f)

        vulnerable_accounts = []

        for acc in accounts:
            sAMAccountName = acc.get("sAMAccountName", "Unknown")
            servicePrincipalName = acc.get("servicePrincipalName", [])
            adminCount = acc.get("adminCount", 0)
            pwdLastSet = acc.get("pwdLastSet", "Unknown")

            # Check if account has an SPN configured
            if servicePrincipalName:
                is_admin = adminCount == 1 or "admin" in sAMAccountName.lower()
                
                vulnerable_accounts.append({
                    "account": sAMAccountName,
                    "spns": servicePrincipalName,
                    "is_privileged": is_admin,
                    "pwd_last_set": pwdLastSet
                })

        print(f"{'sAMAccountName':<20} | {'Privileged':<10} | {'SPN Count':<10} | {'Sample SPN'}")
        print("-" * 75)

        for item in vulnerable_accounts:
            priv_flag = "YES [!]" if item["is_privileged"] else "No"
            sample_spn = item["spns"][0] if isinstance(item["spns"], list) else str(item["spns"])
            print(f"{item['account']:<20} | {priv_flag:<10} | {len(item['spns']):<10} | {sample_spn[:30]}")

        print(f"\n[*] Total SPN-bound Accounts Exposed to Kerberoasting: {len(vulnerable_accounts)}")

    except FileNotFoundError:
        print(f"[-] Error: JSON dataset '{json_input}' not found.")
    except Exception as e:
        print(f"[-] Failed to process directory export: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Identify Kerberoastable Service Principal Name (SPN) accounts in AD exports")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Path to Active Directory user export (JSON format)")

    args = parser.parse_args()
    audit_spn_accounts(args.input)