import re
import sys
import argparse
from pathlib import Path

# Regular expressions for common sensitive token formats
SECRET_PATTERNS = {
    "AWS Access Key": re.compile(r'(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}'),
    "Generic Private Key": re.compile(r'-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY-----'),
    "Slack Token": re.compile(r'xox[baprs]-[0-9]{10,13}-[a-zA-Z0-9-]+'),
    "Generic API Secret Token": re.compile(r'(?i)(api_key|secret_key|auth_token)\s*[:=]\s*["\'][A-Za-z0-9/+=]{16,}["\']')
}

def scan_file_for_secrets(file_path: Path) -> int:
    """Scan a single file for known secret patterns."""
    issues = 0
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_idx, line in enumerate(f, 1):
                for secret_type, regex in SECRET_PATTERNS.items():
                    if regex.search(line):
                        print(f"  [!] {secret_type} found in {file_path}:{line_idx}")
                        issues += 1
    except Exception as e:
        print(f"[-] Error reading {file_path}: {e}")
    return issues

def main() -> None:
    parser = argparse.ArgumentParser(description="Scan local files for sensitive credentials before committing")
    parser.add_argument("files", nargs="+", type=Path, help="List of files to scan")
    args = parser.parse_args()

    total_findings = 0
    print("[+] Running pre-commit credential check...")

    for file_path in args.files:
        if file_path.is_file():
            total_findings += scan_file_for_secrets(file_path)

    if total_findings > 0:
        print(f"\n[CRITICAL] Commit blocked: {total_findings} secret(s) detected. Sanitize code before committing.")
        sys.exit(1)
    else:
        print("[PASS] No hardcoded credentials detected.")
        sys.exit(0)

if __name__ == "__main__":
    main()