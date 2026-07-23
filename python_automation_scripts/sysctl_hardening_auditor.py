import argparse
from pathlib import Path

# Baseline security settings for Linux kernel sysctl
SECURITY_SYSCTL_BASELINE = {
    "net.ipv4.conf.all.accept_redirects": "0",
    "net.ipv4.conf.all.send_redirects": "0",
    "net.ipv4.ip_forward": "0",
    "net.ipv4.tcp_syncookies": "1",
    "kernel.randomize_va_space": "2",  # Full ASLR
    "fs.protected_hardlinks": "1",
    "fs.protected_symlinks": "1"
}

def audit_sysctl_config(config_path: Path) -> None:
    """Compare a sysctl.conf configuration file against hardening baselines."""
    print(f"[+] Auditing sysctl configuration file: {config_path}\n")

    try:
        current_settings = {}
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    current_settings[key.strip()] = val.strip()

        findings = 0
        print(f"{'Parameter':<40} | {'Current':<10} | {'Expected':<10} | {'Status'}")
        print("-" * 75)

        for param, expected_val in SECURITY_SYSCTL_BASELINE.items():
            current_val = current_settings.get(param, "NOT_SET")

            if current_val == expected_val:
                status = "PASS"
            else:
                status = "NON-COMPLIANT"
                findings += 1

            print(f"{param:<40} | {current_val:<10} | {expected_val:<10} | {status}")

        print(f"\n[*] sysctl Audit Complete. Identified {findings} non-compliant kernel setting(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{config_path}' not found.")
    except Exception as e:
        print(f"[-] sysctl audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Linux kernel sysctl settings against security baselines")
    parser.add_argument("-c", "--config", required=True, type=Path, help="Path to sysctl.conf or sysctl dump file")

    args = parser.parse_args()
    audit_sysctl_config(args.config)