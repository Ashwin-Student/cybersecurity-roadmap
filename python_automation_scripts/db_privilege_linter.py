import json
import argparse
from pathlib import Path

ADMIN_PRIVILEGES = {"SUPERUSER", "DBA", "ALL PRIVILEGES", "GRANT OPTION", "DROP DATABASE"}

def audit_db_privileges(user_dump_path: Path) -> None:
    """Scan user definitions for administrative privileges and weak configurations."""
    print(f"[+] Auditing database roles and privilege definitions: {user_dump_path}\n")

    try:
        with open(user_dump_path, "r", encoding="utf-8") as f:
            users = json.load(f)

        findings = 0
        print(f"{'Username':<18} | {'Admin Risk':<12} | {'Password Expiry':<15} | {'Issues'}")
        print("-" * 75)

        for user in users:
            username = user.get("username", "unknown")
            grants = set(user.get("grants", []))
            pass_expires = user.get("password_expires", False)

            matched_admin_privs = grants.intersection(ADMIN_PRIVILEGES)
            is_admin = bool(matched_admin_privs)

            issues = []
            if is_admin:
                issues.append(f"Admin Privileges ({', '.join(matched_admin_privs)})")
            if not pass_expires:
                issues.append("No Password Expiry")

            risk_label = "HIGH" if is_admin else "LOW"
            expiry_str = "Enabled" if pass_expires else "NEVER"

            if issues:
                findings += 1
                print(f"{username:<18} | {risk_label:<12} | {expiry_str:<15} | {'; '.join(issues)}")

        print(f"\n[*] DB Privilege Audit Complete. Flagged {findings} user account(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{user_dump_path}' not found.")
    except Exception as e:
        print(f"[-] Database privilege audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit database accounts for administrative privileges and security settings")
    parser.add_argument("-u", "--users", required=True, type=Path, help="Path to database user metadata JSON")

    args = parser.parse_args()
    audit_db_privileges(args.users)