import math
import argparse
from collections import Counter
from pathlib import Path

def calculate_entropy(text: str) -> float:
    """Calculate Shannon Entropy of a string to measure randomness/encryption."""
    if not text:
        return 0.0
    entropy = 0.0
    for count in Counter(text).values():
        p = count / len(text)
        entropy -= p * math.log2(p)
    return entropy

def analyze_dns_queries(log_file: Path, entropy_threshold: float = 4.2, length_threshold: int = 50) -> None:
    """Audit DNS query logs for high-entropy or unusually long domain requests."""
    print(f"[+] Analyzing DNS query log: {log_file}\n")
    print(f"{'Domain Requested':<45} | {'Length':<8} | {'Entropy':<8} | {'Status'}")
    print("-" * 75)

    flagged_count = 0
    total_queries = 0

    try:
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                domain = line.strip()
                if not domain or domain.startswith("#"):
                    continue

                total_queries += 1
                # Remove TLD to focus on subdomains where data exfiltration occurs
                subdomain_part = domain.split(".")[0]
                entropy = calculate_entropy(subdomain_part)
                length = len(domain)

                if entropy >= entropy_threshold or length >= length_threshold:
                    flagged_count += 1
                    print(f"  [!] {domain:<39} | {length:<8} | {entropy:<8.2f} | TUNNELING RISK")
                
    except FileNotFoundError:
        print(f"[-] Error: DNS log file '{log_file}' not found.")
        return

    print(f"\n[*] Audit Complete: Processed {total_queries} queries.")
    print(f"[*] High-Risk DNS Tunneling Queries Flagged: {flagged_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect DNS exfiltration and high-entropy domain queries")
    parser.add_argument("-l", "--log", required=True, type=Path, help="Path to text file containing DNS queries (one per line)")
    parser.add_argument("-e", "--entropy", type=float, default=4.2, help="Entropy threshold (default: 4.2)")
    parser.add_argument("-m", "--max-len", type=int, default=50, help="Domain length threshold (default: 50)")

    args = parser.parse_args()
    analyze_dns_queries(args.log, args.entropy, args.max_len)