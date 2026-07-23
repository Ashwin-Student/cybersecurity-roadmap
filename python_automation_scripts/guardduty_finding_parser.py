import json
import argparse
from pathlib import Path

def parse_guardduty_findings(json_path: Path) -> None:
    """Parse AWS GuardDuty JSON export and highlight actionable security alerts."""
    print(f"[+] Ingesting AWS GuardDuty findings from: {json_path}\n")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        findings = data if isinstance(data, list) else [data]

        print(f"{'Finding Type':<35} | {'Severity':<8} | {'AccountId':<14} | {'Resource Affected'}")
        print("-" * 80)

        high_severity_count = 0

        for finding in findings:
            finding_type = finding.get("type", "Unknown")
            severity = finding.get("severity", 0.0)
            account_id = finding.get("accountId", "Unknown")
            resource = finding.get("resource", {}).get("resourceType", "Unknown")

            # Classify severity label
            if severity >= 7.0:
                sev_label = "HIGH"
                high_severity_count += 1
            elif severity >= 4.0:
                sev_label = "MEDIUM"
            else:
                sev_label = "LOW"

            print(f"{finding_type[:35]:<35} | {sev_label:<8} | {account_id:<14} | {resource}")

        print(f"\n[*] Total Findings Processed: {len(findings)}")
        print(f"[*] High-Severity Alerts Requiring Immediate Triage: {high_severity_count}")

    except FileNotFoundError:
        print(f"[-] Error: File '{json_path}' not found.")
    except Exception as e:
        print(f"[-] Failed to process GuardDuty export: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse and summarize AWS GuardDuty finding payloads")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Path to GuardDuty JSON findings file")

    args = parser.parse_args()
    parse_guardduty_findings(args.input)