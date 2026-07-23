import json
import argparse
from pathlib import Path

DANGEROUS_KMS_ACTIONS = {"kms:Decrypt", "kms:DisableKey", "kms:ScheduleKeyDeletion", "kms:*"}

def audit_kms_policy(policy_path: Path) -> None:
    """Scan KMS Key Policy for risky public access or broad actions."""
    print(f"[+] Auditing KMS Key Policy: {policy_path}\n")

    try:
        with open(policy_path, "r", encoding="utf-8") as f:
            policy = json.load(f)

        statements = policy.get("Statement", [])
        findings = 0

        for idx, stmt in enumerate(statements, 1):
            effect = stmt.get("Effect", "")
            principal = stmt.get("Principal", {})
            actions = stmt.get("Action", [])

            if isinstance(actions, str):
                actions = [actions]

            if effect == "Allow":
                # Check for public/open principal
                is_public = principal == "*" or principal.get("AWS") == "*"
                
                # Check for sensitive actions
                matched_actions = set(actions).intersection(DANGEROUS_KMS_ACTIONS) or ("*" in actions)

                if is_public:
                    findings += 1
                    print(f"  [CRITICAL] Statement #{idx}: Key allows PUBLIC access ('Principal': '*')!")

                if matched_actions:
                    findings += 1
                    print(f"  [WARNING] Statement #{idx}: Grants high-risk actions -> {list(matched_actions)}")

        print(f"\n[*] KMS Audit Complete. Identified {findings} potential policy risk(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{policy_path}' not found.")
    except Exception as e:
        print(f"[-] Policy parsing failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit AWS KMS Key Policy JSON files for dangerous permissions")
    parser.add_argument("-p", "--policy", required=True, type=Path, help="Path to KMS JSON policy file")

    args = parser.parse_args()
    audit_kms_policy(args.policy)