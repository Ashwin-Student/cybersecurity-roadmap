import re
import argparse
from pathlib import Path

# High-confidence regex patterns for sensitive strings
SECRET_PATTERNS = {
    "AWS Access Key": re.compile(r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}"),
    "Generic API Key": re.compile(r"(?i)(?:api_key|apikey|secret_key|app_secret)\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{16,})['\"]"),
    "RSA Private Key": re.compile(r"-----BEGIN (?:RSA )?PRIVATE KEY-----"),
    "Generic High Entropy Token": re.compile(r"(?i)(?:bearer|token)\s*[:=]\s*['\"]([a-zA-Z0-9_\-\.]{20,})['\"]")
}

IGNORE_DIRS = {".git", "node_modules", "venv", "__pycache__"}

def scan_file_for_secrets(file_path: Path) -> int:
    """Scan an individual text file against high-risk regex patterns."""
    findings = 0
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                for label, pattern in SECRET_PATTERNS.items():
                    if pattern.search(line):
                        print(f"  [!] {label:<22} | Line {line_num:<4} in {file_path}")
                        findings += 1
    except Exception:
        pass
    return findings

def scan_directory(target_dir: Path) -> None:
    """Traverse local directory and audit files for committed secrets."""
    print(f"[+] Scanning directory for exposed secrets: {target_dir}\n")
    total_findings = 0
    total_files = 0

    for path in target_dir.rglob("*"):
        # Skip ignored directories
        if any(part in IGNORE_DIRS for part in path.parts):
            continue

        if path.is_file() and not path.name.endswith((".png", ".jpg", ".zip", ".exe", ".pyc")):
            total_files += 1
            total_findings += scan_file_for_secrets(path)

    print(f"\n--- Scan Complete ---")
    print(f"Files Inspected: {total_files}")
    print(f"Secrets Identified: {total_findings}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan local repository files for hardcoded secrets")
    parser.add_argument("-d", "--dir", default=Path("."), type=Path, help="Target directory (default: current directory)")

    args = parser.parse_args()
    scan_directory(args.dir)