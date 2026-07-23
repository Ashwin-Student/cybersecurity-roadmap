import os
import argparse
try:
    import psutil
except ImportError:
    raise SystemExit("[-] Missing dependency! Install psutil via: pip install psutil")

# Directories commonly associated with temporary file execution or staging
SUSPICIOUS_PATHS_POSIX = ["/tmp", "/var/tmp", "/dev/shm", "/run/user"]
SUSPICIOUS_PATHS_WIN = ["\\appdata\\local\\temp", "\\windows\\temp", "\\public"]

def inspect_running_processes() -> None:
    """Inspect process execution paths for unexpected temporary locations."""
    print("\n--- Running Process Path Analysis ---")
    
    suspicious_dirs = SUSPICIOUS_PATHS_WIN if os.name == "nt" else SUSPICIOUS_PATHS_POSIX
    suspicious_found = False

    for proc in psutil.process_iter(['pid', 'name', 'exe', 'username']):
        try:
            exe_path = proc.info.get('exe')
            if not exe_path:
                continue

            exe_lower = exe_path.lower()
            for path in suspicious_dirs:
                if path in exe_lower:
                    suspicious_found = True
                    print(f"[!] SUSPICIOUS PROCESS LOCATION DETECTED:")
                    print(f"    PID:      {proc.info['pid']}")
                    print(f"    Name:     {proc.info['name']}")
                    print(f"    User:     {proc.info['username']}")
                    print(f"    Path:     {exe_path}\n")
                    break

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if not suspicious_found:
        print("[+] STATUS: All inspected processes running from standard system locations.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit processes executing from temporary directories")
    args = parser.parse_args()
    inspect_running_processes()