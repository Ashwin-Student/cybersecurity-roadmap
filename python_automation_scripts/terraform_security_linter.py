import re
import argparse
from pathlib import Path

# Common Terraform security antipatterns
CHECKS = [
    {
        "id": "TF-SEC-01",
        "name": "Open Security Group Ingress",
        "pattern": re.compile(r'cidr_blocks\s*=\s*\[\s*"0\.0\.0\.0/0"\s*\]'),
        "severity": "HIGH",
        "recommendation": "Restrict inbound traffic to specific CIDR blocks."
    },
    {
        "id": "TF-SEC-02",
        "name": "Unencrypted S3 Bucket",
        "pattern": re.compile(r'rule\s*\{[^}]*apply_server_side_encryption_by_default'),
        "severity": "MEDIUM",
        "invert": True,  # Flag if pattern is MISSING in aws_s3_bucket
        "recommendation": "Ensure default server-side encryption is enabled."
    },
    {
        "id": "TF-SEC-03",
        "name": "Hardcoded Secret / Password",
        "pattern": re.compile(r'(?i)(?:password|secret|key)\s*=\s*"[^"${}]{6,}"'),
        "severity": "CRITICAL",
        "recommendation": "Use environment variables or secrets manager references."
    }
]

def lint_terraform_file(tf_path: Path) -> int:
    """Scan a Terraform template for security misconfigurations."""
    print(f"[+] Auditing Terraform configuration: {tf_path}\n")
    findings = 0

    try:
        with open(tf_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        for check in CHECKS:
            match = check["pattern"].search(content)
            should_flag = match if not check.get("invert") else not match

            if should_flag:
                findings += 1
                print(f"  [{check['severity']}] {check['id']}: {check['name']}")
                print(f"         Recommendation: {check['recommendation']}\n")

        print(f"--- Summary ---")
        print(f"Total Policy Violations Found: {findings}")

    except FileNotFoundError:
        print(f"[-] Error: File '{tf_path}' not found.")
    return findings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lint Terraform (.tf) templates for security misconfigurations")
    parser.add_argument("-f", "--file", required=True, type=Path, help="Path to .tf configuration file")

    args = parser.parse_args()
    lint_terraform_file(args.file)