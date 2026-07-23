import subprocess
import json
import argparse
from pathlib import Path

def get_installed_linux_packages() -> dict:
    """Retrieve installed DEB/RPM package names and versions."""
    packages = {}
    try:
        # Try dpkg first (Debian/Ubuntu)
        res = subprocess.run(["dpkg-query", "-W", "-f=${Package}|${Version}\n"], capture_output=True, text=True)
        if res.returncode == 0:
            for line in res.stdout.splitlines():
                if "|" in line:
                    pkg, ver = line.split("|", 1)
                    packages[pkg] = ver
            return packages
    except FileNotFoundError:
        pass

    try:
        # Try rpm (RHEL/CentOS)
        res = subprocess.run(["rpm", "-qa", "--qf", "%{NAME}|%{VERSION}\n"], capture_output=True, text=True)
        if res.returncode == 0:
            for line in res.stdout.splitlines():
                if "|" in line:
                    pkg, ver = line.split("|", 1)
                    packages[pkg] = ver
    except FileNotFoundError:
        pass

    return packages

def audit_software_inventory(vuln_db_path: Path) -> None:
    """Compare local package inventory against a list of known vulnerable software versions."""
    print("[+] Gathering installed system packages...")
    installed_pkgs = get_installed_linux_packages()

    if not installed_pkgs:
        print("[-] Unable to query package manager or non-Linux system.")
        return

    print(f"[+] Total Installed Packages Identified: {len(installed_pkgs)}")
    print(f"[+] Loading vulnerable software baseline from: {vuln_db_path}\n")

    try:
        with open(vuln_db_path, "r", encoding="utf-8") as f:
            vulnerable_db = json.load(f)

        findings = 0
        print(f"{'Package Name':<25} | {'Installed Version':<18} | {'Vulnerable Version'}")
        print("-" * 65)

        for pkg, installed_ver in installed_pkgs.items():
            if pkg in vulnerable_db:
                vuln_ver = vulnerable_db[pkg]
                if installed_ver.startswith(vuln_ver):
                    findings += 1
                    print(f"  [!] {pkg:<21} | {installed_ver:<18} | {vuln_ver}")

        print(f"\n[*] Audit Complete: Flagged {findings} vulnerable package match(es).")

    except FileNotFoundError:
        print(f"[-] Vulnerability database file '{vuln_db_path}' not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit installed software inventory against vulnerable version baselines")
    parser.add_argument("-db", "--vuln-db", required=True, type=Path, help="JSON database of vulnerable packages (e.g., {'openssl': '1.1.1a'})")

    args = parser.parse_args()
    audit_software_inventory(args.vuln_db)