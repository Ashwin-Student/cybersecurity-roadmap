import json
import argparse
from datetime import datetime
from pathlib import Path

def audit_domain_expirations(domains_json: Path) -> None:
    """Audit domain inventory for upcoming expiration dates and risk of drop-registration."""
    print(f"[+] Auditing domain registration expirations: {domains_json}\n")

    try:
        with open(domains_json, "r", encoding="utf-8") as f:
            domains = json.load(f)

        now = datetime.utcnow()
        at_risk = 0

        print(f"{'Domain Name':<30} | {'Registrar':<20} | {'Days Left':<10} | {'Risk Level'}")
        print("-" * 75)

        for item in domains:
            domain = item.get("domain", "unknown")
            registrar = item.get("registrar", "Unknown")[:19]
            exp_str = item.get("expiration_date")

            if not exp_str:
                continue

            exp_dt = datetime.fromisoformat(exp_str.replace("Z", ""))
            days_remaining = (exp_dt - now).days

            if days_remaining <= 0:
                risk = "EXPIRED [!]"
                at_risk += 1
            elif days_remaining <= 30:
                risk = "CRITICAL (<30 days)"
                at_risk += 1
            elif days_remaining <= 90:
                risk = "WARNING (<90 days)"
            else:
                risk = "LOW"

            print(f"{domain:<30} | {registrar:<20} | {days_remaining:<10} | {risk}")

        print(f"\n[*] WHOIS Expiration Audit Complete. {at_risk} domain(s) require renewal.")

    except FileNotFoundError:
        print(f"[-] Error: File '{domains_json}' not found.")
    except Exception as e:
        print(f"[-] WHOIS audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit domain registration expiration dates for hijacking prevention")
    parser.add_argument("-j", "--json", required=True, type=Path, help="Path to domain WHOIS metadata JSON")

    args = parser.parse_args()
    audit_domain_expirations(args.json)