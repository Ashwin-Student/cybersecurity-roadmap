import argparse
from pathlib import Path

# Recommended settings for secure SSH server operation
RECOMMENDED_SETTINGS = {
    "PermitRootLogin": ["no", "prohibit-password"],
    "PasswordAuthentication": ["no"],
    "X11Forwarding": ["no"],
    "MaxAuthTries": ["3", "4"],
    "AllowTcpForwarding": ["no"]
}

def audit_sshd_config(config_path: Path) -> None:
    """Audit OpenSSH daemon configuration against security hardening directives."""
    print(f"[+] Auditing SSH daemon configuration: {config_path}\n")

    try:
        settings = {}
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0]
                    value = parts[1].lower()
                    settings[key] = value

        findings = 0
        print(f"{'Directive':<25} | {'Current Setting':<15} | {'Compliance Status'}")
        print("-" * 65)

        for directive, valid_values in RECOMMENDED_SETTINGS.items():
            current = settings.get(directive, "default (unspecified)")
            if current in valid_values:
                status = "PASS"
            else:
                status = f"WARN (Expected: {', '.join(valid_values)})"
                findings += 1

            print(f"{directive:<25} | {current:<15} | {status}")

        print(f"\n[*] Audit Complete. Identified {findings} potential hardening recommendation(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{config_path}' not found.")
    except Exception as e:
        print(f"[-] SSH config audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit OpenSSH sshd_config file against security benchmarks")
    parser.add_argument("-c", "--config", required=True, type=Path, help="Path to sshd_config file")

    args = parser.parse_args()
    audit_sshd_config(args.config)