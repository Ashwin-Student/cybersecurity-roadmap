import os
import stat
import argparse
from pathlib import Path

CRON_DIRS = [Path("/etc/cron.d"), Path("/etc/cron.daily"), Path("/etc/cron.hourly"), Path("/etc/crontab")]

def audit_cron_integrity() -> None:
    """Inspect system cron directories for unsafe permissions and unquoted execution paths."""
    print("[+] Auditing system cron configurations and file permissions...\n")

    findings = 0
    print(f"{'Path':<45} | {'Owner / Perms':<18} | {'Security Issue'}")
    print("-" * 80)

    for path in CRON_DIRS:
        if not path.exists():
            continue

        target_files = [path] if path.is_file() else list(path.glob("*"))

        for file_path in target_files:
            if not file_path.is_file():
                continue

            try:
                st = file_path.stat()
                mode = st.st_mode
                is_world_writable = bool(mode & stat.S_IWOTH)

                perms_str = oct(mode)[-3:]

                if is_world_writable:
                    findings += 1
                    print(f"{str(file_path):<45} | {perms_str:<18} | CRITICAL (World-Writable Cron File)")

                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        line_str = line.strip()
                        if line_str and not line_str.startswith("#"):
                            # Check for writable script targets inside cron lines
                            parts = line_str.split()
                            for part in parts:
                                if part.startswith("/") and Path(part).exists():
                                    target_st = Path(part).stat()
                                    if target_st.st_mode & stat.S_IWOTH:
                                        findings += 1
                                        print(f"{str(file_path):<45} | Line {line_num:<13} | HIGH (Executes World-Writable Binary: {part})")

            except Exception as e:
                print(f"[-] Error reading {file_path}: {e}")

    print(f"\n[*] Cron Integrity Audit Complete. Identified {findings} potential task integrity risk(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit system cron configuration files for weak permissions and execution risks")
    parser.parse_args()
    audit_cron_integrity()