import os
from pathlib import Path
import argparse

CRON_LOCATIONS = [
    Path("/etc/crontab"),
    Path("/etc/cron.dhourly"),
    Path("/etc/cron.daily"),
    Path("/etc/cron.weekly"),
    Path("/etc/cron.monthly"),
    Path("/etc/cron.d"),
    Path("/var/spool/cron/crontabs")
]

def audit_cron_jobs() -> None:
    """Inspect Linux scheduled task directories for suspicious configurations."""
    print("--- Cron Scheduled Job Auditor ---\n")

    for location in CRON_LOCATIONS:
        if not location.exists():
            continue

        print(f"[+] Inspecting: {location}")

        if location.is_file():
            _check_file_content(location)
        elif location.is_dir():
            for entry in location.iterdir():
                if entry.is_file() and not entry.name.startswith("."):
                    _check_file_content(entry)

def _check_file_content(file_path: Path) -> None:
    """Read cron file and highlight commands executing from temporary directories or shell scripts."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip()
                # Skip comments and empty lines
                if not clean_line or clean_line.startswith("#"):
                    continue

                # Flag cron entries referencing temporary or hidden locations
                if any(x in clean_line for x in ["/tmp", "/dev/shm", "curl", "wget", "python", "bash"]):
                    print(f"    [!] Line {line_num:<3} in {file_path.name}:")
                    print(f"        Command: {clean_line}")

    except PermissionError:
        print(f"    [-] Permission Denied: Unable to read {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan local cron directories for persistence artifacts")
    args = parser.parse_args()

    if os.name != "posix":
        print("[-] This script is intended for POSIX/Linux cron auditing.")
    else:
        audit_cron_jobs()