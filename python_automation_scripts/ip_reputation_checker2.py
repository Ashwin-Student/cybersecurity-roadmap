import json
import argparse
from pathlib import Path

HIGH_RISK_CATEGORIES = {"botnet", "tor_exit_node", "malware_c2", "scanners"}

def audit_ip_reputation(threat_data_file: Path) -> None:
    """Evaluate IP threat intelligence score metadata for network indicators."""
    print(f"[+] Evaluating IP Threat Intelligence metadata: {threat_data_file}\n")

    try:
        with open(threat_data_file, "r", encoding="utf-8") as f:
            records = json.load(f)

        flagged_count = 0
        print(f"{'IP Address':<18} | {'Reputation Score':<18} | {'ASN / Org':<20} | {'Threat Category'}")
        print("-" * 80)

        for entry in records:
            ip = entry.get("ip", "0.0.0.0")
            score = entry.get("reputation_score", 0)  # 0 to 100 scale
            asn = entry.get("asn_org", "Unknown")[:19]
            categories = set(entry.get("categories", []))

            is_high_risk = score >= 75 or bool(categories.intersection(HIGH_RISK_CATEGORIES))

            if is_high_risk:
                flagged_count += 1
                status_cat = f"FLAGGED ({', '.join(categories)})" if categories else "HIGH RISK"
            else:
                status_cat = "CLEAN / LOW"

            score_str = f"{score}/100"

            print(f"{ip:<18} | {score_str:<18} | {asn:<20} | {status_cat}")

        print(f"\n[*] Threat Intel Complete. Flagged {flagged_count} malicious or high-risk IP(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{threat_data_file}' not found.")
    except Exception as e:
        print(f"[-] Reputation check failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit IP reputation indicators against threat intelligence data")
    parser.add_argument("-f", "--file", required=True, type=Path, help="Path to IP threat intelligence JSON file")

    args = parser.parse_args()
    audit_ip_reputation(args.file)