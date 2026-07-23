import argparse
from pathlib import Path

PAM_SECURITY_MODULES = {
    "pam_pwquality.so": "Enforces strong password complexity rules",
    "pam_faillock.so": "Locks accounts after consecutive failed attempts",
    "pam_pwhistory.so": "Prevents recent password reuse"
}

def audit_pam_config(pam_path: Path) -> None:
    """Check PAM configuration files for required security enforcement modules."""
    print(f"[+] Auditing PAM authentication module file: {pam_path}\n")

    try:
        with open(pam_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        content = " ".join([line.strip() for line in lines if not line.strip().startswith("#")])
        findings = 0

        print(f"{'PAM Module':<20} | {'Status':<12} | {'Description'}")
        print("-" * 75)

        for module, desc in PAM_SECURITY_MODULES.items():
            if module in content:
                status = "PRESENT"
            else:
                status = "MISSING [!]"
                findings += 1

            print(f"{module:<20} | {status:<12} | {desc}")

        print(f"\n[*] PAM Configuration Audit Complete. {findings} security module(s) missing.")

    except FileNotFoundError:
        print(f"[-] Error: File '{pam_path}' not found.")
    except Exception as e:
        print(f"[-] PAM configuration audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Linux PAM setup files for pwquality, faillock, and pwhistory")
    parser.add_argument("-p", "--pamfile", required=True, type=Path, help="Path to PAM config file (e.g., /etc/pam.d/common-password)")

    args = parser.parse_args()
    audit_pam_config(args.pamfile)import argparse
from pathlib import Path

PAM_SECURITY_MODULES = {
    "pam_pwquality.so": "Enforces strong password complexity rules",
    "pam_faillock.so": "Locks accounts after consecutive failed attempts",
    "pam_pwhistory.so": "Prevents recent password reuse"
}

def audit_pam_config(pam_path: Path) -> None:
    """Check PAM configuration files for required security enforcement modules."""
    print(f"[+] Auditing PAM authentication module file: {pam_path}\n")

    try:
        with open(pam_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        content = " ".join([line.strip() for line in lines if not line.strip().startswith("#")])
        findings = 0

        print(f"{'PAM Module':<20} | {'Status':<12} | {'Description'}")
        print("-" * 75)

        for module, desc in PAM_SECURITY_MODULES.items():
            if module in content:
                status = "PRESENT"
            else:
                status = "MISSING [!]"
                findings += 1

            print(f"{module:<20} | {status:<12} | {desc}")

        print(f"\n[*] PAM Configuration Audit Complete. {findings} security module(s) missing.")

    except FileNotFoundError:
        print(f"[-] Error: File '{pam_path}' not found.")
    except Exception as e:
        print(f"[-] PAM configuration audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Linux PAM setup files for pwquality, faillock, and pwhistory")
    parser.add_argument("-p", "--pamfile", required=True, type=Path, help="Path to PAM config file (e.g., /etc/pam.d/common-password)")

    args = parser.parse_args()
    audit_pam_config(args.pamfile)