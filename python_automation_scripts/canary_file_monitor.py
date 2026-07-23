import os
import hashlib
import time
import argparse
from pathlib import Path

def compute_hash(file_path: Path) -> str:
    """Compute SHA256 hash of canary file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def monitor_canary(canary_path: Path, check_interval: int = 5) -> None:
    """Continuously monitor a canary file for unauthorized access, modification, or deletion."""
    if not canary_path.exists():
        print(f"[-] Error: Canary file '{canary_path}' does not exist.")
        return

    print(f"[+] Initializing Canary File Sentinel for: {canary_path}")
    initial_hash = compute_hash(canary_path)
    print(f"[+] Baseline SHA256: {initial_hash}")
    print(f"[+] Active Sentinel running (polling every {check_interval}s)...\n")

    try:
        while True:
            time.sleep(check_interval)

            if not canary_path.exists():
                print(f"[CRITICAL ALERT] CANARY FILE DELETED OR RENAMED: {canary_path}")
                print("                 Possible ransomware/destruction activity detected!")
                break

            current_hash = compute_hash(canary_path)
            if current_hash != initial_hash:
                print(f"[CRITICAL ALERT] CANARY FILE MODIFIED: {canary_path}")
                print(f"                 Original Hash: {initial_hash}")
                print(f"                 Current Hash:  {current_hash}")
                break

    except KeyboardInterrupt:
        print("\n[*] Sentinel monitoring stopped by operator.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor a honeypot canary file for tampering/ransomware activity")
    parser.add_argument("-c", "--canary", required=True, type=Path, help="Path to canary file")
    parser.add_argument("-i", "--interval", type=int, default=5, help="Polling interval in seconds")

    args = parser.parse_args()
    monitor_canary(args.canary, args.interval)