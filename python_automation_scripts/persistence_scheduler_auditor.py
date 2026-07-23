import os
import sys
import argparse
from pathlib import Path

CRON_LOCATIONS = [
    Path("/etc/crontab"),
    Path("/etc/cron.hourly"),
    Path("/etc/cron.daily"),
    Path("/etc/cron.weekly"),
    Path("/etc/cron.monthly"),
    Path("/var/spool/cron/crontabs")
]

def audit_cron_jobs() -> None:
    """Inspect system cron directories for non-standard or unauthorized jobs."""
    if sys.platform.startswith("win"):
        print("[-] This script is configured for POSIX/Linux persistence auditing.")
        return

    print("--- Local Cron Persistence Audit ---\n")
    found_jobs = 0

    for path in CRON_LOCATIONS:
        if not path.exists():
            continue

        if path.is_file():
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
                    if lines:
                        print(f"[+] File: {path}")
                        for line in lines:
                            print(f"    {line}")
                            found_jobs += 1
            except PermissionError:
                print(f"[-] Permission Denied reading: {path}")

        elif path.is_dir():
            print(f"[+] Inspecting Directory: {path}")
            try:
                for cron_file in path.iterdir():
                    if cron_file.is_file() and not cron_file.name.startswith("."):
                        print(f"    -> Scheduled Item: {cron_file.name}")
                        found_jobs += 1
            except PermissionError:
                print(f"[-] Permission Denied traversing: {path}")

    print(f"\n[*] Persistence Check Complete: {found_jobs} scheduled items evaluated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit system cron configuration paths for persistence mechanisms")
    args = parser.parse_args()
    audit_cron_jobs()