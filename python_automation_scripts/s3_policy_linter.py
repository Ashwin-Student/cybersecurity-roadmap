import json
import argparse
from pathlib import Path

def lint_s3_policy(policy_path: Path) -> None:
    """Audit S3 bucket policy JSON definitions for public or permissive statements."""
    print(f"[+] Linting AWS S3 Bucket Policy: {policy_path}\n")

    try:
        with open(policy_path, "r", encoding="utf-8") as f:
            policy = json.load(f)

        statements = policy.get("Statement", [])
        findings = 0

        print(f"{'Statement ID':<15} | {'Effect':<8} | {'Principal':<15} | {'Risk Flag'}")
        print("-" * 75)

        has_https_enforcement = False

        for stmt in statements:
            sid = stmt.get("Sid", "NoSid")[:14]
            effect = stmt.get("Effect", "Allow")
            principal = stmt.get("Principal", {})
            condition = stmt.get("Condition", {})

            # Check 1: Wildcard Principal
            is_wildcard_principal = principal == "*" or (isinstance(principal, dict) and principal.get("AWS") == "*")

            # Check 2: Check HTTPS enforcement condition
            if effect == "Deny" and "Bool" in condition:
                if condition["Bool"].get("aws:SecureTransport") in ["false", False]:
                    has_https_enforcement = True

            if effect == "Allow" and is_wildcard_principal:
                findings += 1
                print(f"{sid:<15} | {effect:<8} | {'* (Public)':<15} | CRITICAL (Public Access Allowed)")
            elif effect == "Allow" and not condition:
                findings += 1
                print(f"{sid:<15} | {effect:<8} | {str(principal):<15} | WARN (Unconditioned Allow)")

        if not has_https_enforcement:
            findings += 1
            print(f"{'POLICY':<15} | {'WARN':<8} | {'N/A':<15} | Missing explicit HTTPS enforcement (aws:SecureTransport)")

        print(f"\n[*] S3 Policy Audit Complete. Flagged {findings} potential policy weakness(es).")

    except FileNotFoundError:
        print(f"[-] Error: File '{policy_path}' not found.")
    except Exception as e:
        print(f"[-] S3 policy linting failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit S3 bucket policy JSON files for public exposure risks")
    parser.add_argument("-p", "--policy", required=True, type=Path, help="Path to S3 bucket policy JSON file")

    args = parser.parse_args()
    lint_s3_policy(args.policy)