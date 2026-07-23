import argparse
from pathlib import Path

REQUIRED_AUDIT_KEYS = {
    "-w /etc/passwd": "User Account Changes",
    "-w /etc/shadow": "Credential Store Monitoring",
    "-w /etc/sudoers": "Sudoers Policy Changes",
    "-a always,exit": "Systemcall Auditing",
    "-k time-change": "System Clock Changes"
}

def audit_auditd_rules(rules_path: Path) -> None:
    """Verify presence of key security monitoring directives in Auditd configuration."""
    print(f"[+] Auditing Linux Auditd configuration rules: {rules_path}\n")

    try:
        with open(rules_path, "r", encoding="utf-8") as f:
            content = f.read()

        findings = 0
        print(f"{'Required Control':<30} | {'Status':<12} | {'Description'}")
        print("-" * 75)

        for rule_pattern, description in REQUIRED_AUDIT_KEYS.items():
            if rule_pattern in content:
                status = "PASS"
            else:
                status = "MISSING [!]"
                findings += 1

            print(f"{rule_pattern:<30} | {status:<12} | {description}")

        print(f"\n[*] Auditd Rule Verification Complete. {findings} critical control rule(s) missing.")

    except FileNotFoundError:
        print(f"[-] Error: File '{rules_path}' not found.")
    except Exception as e:
        print(f"[-] Auditd rule inspection failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Linux Auditd rules for essential compliance logging requirements")
    parser.add_argument("-r", "--rules", required=True, type=Path, help="Path to audit.rules file")

    args = parser.parse_args()
    audit_auditd_rules(args.rules)