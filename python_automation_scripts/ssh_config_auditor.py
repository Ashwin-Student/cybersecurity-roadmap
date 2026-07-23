import os
import stat
import argparse
from pathlib import Path

def check_private_key_permissions(ssh_dir: Path) -> int:
    """Check if SSH private keys have secure POSIX permissions."""
    print(f"[+] Auditing SSH directory: {ssh_dir}\n")
    violations = 0

    if not ssh_dir.exists():
        print(f"[-] Directory '{ssh_dir}' does not exist.")
        return 0

    for item in ssh_dir.iterdir():
        if item.is_file() and not item.name.endswith(".pub") and "id_" in item.name:
            file_stat = item.stat()
            permissions = oct(file_stat.st_mode & 0o777)

            # Insecure if group or world can read/write/execute
            if file_stat.st_mode & (stat.S_IRWXG | stat.S_IRWXO):
                violations += 1
                print(f"  [!] RISKY PERMISSIONS: {item.name}")
                print(f"      Current Mode: {permissions} (Expected: 0o600 or 0o400)")
                print(f"      Fix Command : chmod 600 {item.absolute()}\n")
            else:
                print(f"  [PASS] {item.name:<20} | Permissions: {permissions}")

    return violations

def audit_sshd_config(config_path: Path) -> None:
    """Audit system sshd_config for common hardening best practices."""
    print(f"\n[+] Auditing OpenSSH Server Config: {config_path}\n")

    hardening_checks = {
        "PermitRootLogin": "no",
        "PasswordAuthentication": "no",
        "X11Forwarding": "no",
        "MaxAuthTries": "3"
    }

    if not config_path.exists():
        print(f"[-] Configuration file '{config_path}' not found.")
        return

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        config_map = {}
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 2:
                    config_map[parts[0]] = parts[1]

        for setting, recommended in hardening_checks.items():
            actual = config_map.get(setting, "Default / Not Set")
            status = "PASS" if actual.lower() == recommended.lower() else "WARN"
            print(f"  [{status}] {setting:<24} | Current: {actual:<15} | Recommended: {recommended}")

    except Exception as e:
        print(f"[-] Failed to read sshd_config: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit local SSH keys permissions and server config")
    parser.add_argument("-k", "--key-dir", type=Path, default=Path.home() / ".ssh", help="Path to SSH key directory")
    parser.add_argument("-c", "--config", type=Path, default=Path("/etc/ssh/sshd_config"), help="Path to sshd_config file")

    args = parser.parse_args()
    check_private_key_permissions(args.key-dir)
    audit_sshd_config(args.config)