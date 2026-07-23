import json
import argparse
from pathlib import Path

HIGH_RISK_ACTIONS = {
    "*",
    "iam:*",
    "s3:*",
    "ec2:*",
    "sts:assumerole",
    "iam:passrole",
    "iam:createaccesskey"
}

def audit_iam_policy(policy_path: Path) -> None:
    """Analyze IAM policy JSON for wildcard administrative permissions."""
    print(f"[+] Loading IAM Policy document: {policy_path}\n")

    try:
        with open(policy_path, "r", encoding="utf-8") as f:
            policy_data = json.load(f)

        statements = policy_data.get("Statement", [])
        if isinstance(statements, dict):
            statements = [statements]

        findings = 0
        print(f"{'Statement ID':<20} | {'Effect':<8} | {'Risk Level':<10} | {'Details'}")
        print("-" * 75)

        for idx, stmt in enumerate(statements, 1):
            sid = stmt.get("Sid", f"Statement_{idx}")
            effect = stmt.get("Effect", "Allow")
            actions = stmt.get("Action", [])
            resource = stmt.get("Resource", "")

            if isinstance(actions, str):
                actions = [actions]

            if effect == "Allow":
                # Check for wildcards in Action or Resource
                has_wildcard_action = any(act.lower() in HIGH_RISK_ACTIONS for act in actions)
                has_wildcard_resource = resource == "*"

                if has_wildcard_action and has_wildcard_resource:
                    findings += 1
                    print(f"{sid:<20} | {effect:<8} | CRITICAL   | Full Admin Wildcard (* on *)")
                elif has_wildcard_action:
                    findings += 1
                    print(f"{sid:<20} | {effect:<8} | HIGH       | Over-privileged Action(s): {actions}")
                elif has_wildcard_resource:
                    findings += 1
                    print(f"{sid:<20} | {effect:<8} | MEDIUM     | Unscoped Resource (*)")

        print(f"\n[*] Audit Complete: Identified {findings} potential policy misconfigurations.")

    except FileNotFoundError:
        print(f"[-] Error: File '{policy_path}' not found.")
    except json.JSONDecodeError:
        print("[-] Error: Invalid JSON syntax in policy document.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Cloud IAM Policies for excessive privileges")
    parser.add_argument("-p", "--policy", required=True, type=Path, help="Path to IAM Policy JSON file")

    args = parser.parse_args()
    audit_iam_policy(args.policy)