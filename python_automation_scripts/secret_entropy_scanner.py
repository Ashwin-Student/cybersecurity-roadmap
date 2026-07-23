import math
import argparse
from pathlib import Path

# Common extensions to audit
AUDIT_EXTENSIONS = {".py", ".json", ".yaml", ".yml", ".env", ".js", ".ts", ".conf", ".ini"}

def calculate_shannon_entropy(data: str) -> float:
    """Calculate the Shannon Entropy of a string to detect randomness/keys."""
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    for count in set(data):
        p_x = data.count(count) / length
        entropy -= p_x * math.log2(p_x)
    return entropy

def scan_directory_for_secrets(target_dir: Path, threshold: float = 4.5) -> None:
    """Scan codebases for suspicious high-entropy strings."""
    print(f"[+] Scanning directory for potential exposed secrets: {target_dir}")
    print(f"[+] Using Shannon Entropy Threshold: {threshold}\n")

    findings = 0

    for path in target_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in AUDIT_EXTENSIONS:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        words = line.strip().split()
                        for word in words:
                            # Strip quotes and common delimiters
                            cleaned_word = word.strip("'\"=;:,")
                            if len(cleaned_word) > 16:  # High-entropy candidate length
                                entropy = calculate_shannon_entropy(cleaned_word)
                                if entropy >= threshold:
                                    findings += 1
                                    print(f"  [!] High Entropy ({entropy:.2f}) -> {path.name}:{line_num}")
                                    print(f"      Candidate: {cleaned_word[:10]}...{cleaned_word[-4:]}\n")

            except Exception as e:
                continue

    print(f"[*] Scan Complete. Total Suspicious High-Entropy Tokens Found: {findings}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan source directories for hardcoded secrets using Shannon Entropy")
    parser.add_argument("-d", "--dir", required=True, type=Path, help="Path to source code directory")
    parser.add_argument("-t", "--threshold", type=float, default=4.5, help="Entropy threshold (default: 4.5)")

    args = parser.parse_args()
    scan_directory_for_secrets(args.dir, args.threshold)