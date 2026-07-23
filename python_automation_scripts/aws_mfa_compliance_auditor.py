import json
import argparse
from pathlib import Path

def audit_mfa_compliance(credential_report_path: Path) -> None:
    """Audit IAM user credential metadata for missing MFA configuration."""
    print(f"[+] Auditing IAM user MFA compliance: {credential_report_path}\n")

    try:
        with open(credential_report_path, "r", encoding="utf-8") as f:
            users = json.load(f)

        non_compliant_users = 0
        print(f"{'User Name':<20} | {'Console Access':<15} | {'MFA Active':<12} | {'Compliance Status'}")
        print("-" * 75)

        for user in users:
            username = user.get("user", "unknown")
            password_enabled = user.get("password_enabled", False)
            mfa_active = user.get("mfa_active", False)

            if password_enabled and not mfa_active:
                status = "NON-COMPLIANT [!]"
                non_compliant_users += 1
            elif not password_enabled and not mfa_active:
                status = "API-ONLY (No Password)"
            else:
                status = "COMPLIANT"

            console_str = "Enabled" if password_enabled else "Disabled"
            mfa_str = "Yes" if mfa_active else "No"

            print(f"{username:<20} | {console_str:<15} | {mfa_str:<12} | {status}")

        print(f"\n[*] Audit Complete. Found {non_compliant_users} console user(s) lacking MFA.")

    except FileNotFoundError:
        print(f"[-] Error: File '{credential_report_path}' not found.")
    except Exception as e:
        print(f"[-] MFA audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit AWS IAM user reports for missing MFA enforcement")
    parser.add_argument("-r", "--report", required=True, type=Path, help="Path to IAM credential report JSON")

    args = parser.parse_args()
    audit_mfa_compliance(args.report)