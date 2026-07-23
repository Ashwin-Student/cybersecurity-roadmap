import argparse
from pathlib import Path
try:
    import psutil
except ImportError:
    raise SystemExit("[-] Missing dependency! Install via: pip install psutil")

# Suspicious path indicators (e.g., binaries executing from temporary/unusual locations)
SUSPICIOUS_PATHS = {"/tmp", "/var/tmp", "c:\\temp", "c:\\users\\public", "appdata\\local\\temp"}

def audit_process_memory() -> None:
    """Inspect active system processes and flag unusual binary executing paths."""
    print("--- Running Processes & Memory Path Audit ---\n")
    print(f"{'PID':<7} | {'Process Name':<20} | {'Status':<10} | {'Executable Path'}")
    print("-" * 75)

    flagged_count = 0
    total_scanned = 0

    for proc in psutil.process_iter(attrs=["pid", "name", "exe", "status"]):
        try:
            total_scanned += 1
            info = proc.info
            pid = info["pid"]
            name = info["name"] or "Unknown"
            status = info["status"]
            exe_path = info["exe"] or "N/A"

            # Check if execution path contains temporary or non-standard directories
            exe_lower = exe_path.lower()
            is_suspicious = any(susp in exe_lower for susp in SUSPICIOUS_PATHS)

            if is_suspicious:
                flagged_count += 1
                print(f"[!] ALERT | {pid:<5} | {name:<20} | {status:<10} | {exe_path}")
            else:
                # Normal operational output for privileged processes
                pass

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    print(f"\n[*] Audit Complete: Scanned {total_scanned} processes.")
    print(f"[*] Flagged Processes in Temporary/Suspicious Directories: {flagged_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit running system processes for execution from non-standard paths")
    args = parser.parse_args()
    audit_process_memory()