import argparse
from pathlib import Path

# USB Class Codes
USB_CLASS_MASS_STORAGE = "08"
USB_CLASS_HID          = "03"

def audit_usb_rules(rules_path: Path) -> None:
    """Inspect USBGuard policy configuration for permissive device rules."""
    print(f"[+] Auditing USB authorization rules: {rules_path}\n")

    try:
        with open(rules_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        findings = 0
        print(f"{'Rule Line':<10} | {'Action':<10} | {'Target Class':<18} | {'Security Risk'}")
        print("-" * 75)

        for idx, line in enumerate(lines, 1):
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue

            parts = clean_line.split()
            action = parts[0] if parts else "unknown"

            if action == "allow":
                if f"with-interface {USB_CLASS_MASS_STORAGE}" in clean_line or "bInterfaceClass=08" in clean_line:
                    findings += 1
                    print(f"{idx:<10} | {'ALLOW':<10} | {'Mass Storage (08)':<18} | HIGH (Data Exfiltration Risk)")

                elif "with-connect-type" not in clean_line and "id *" in clean_line:
                    findings += 1
                    print(f"{idx:<10} | {'ALLOW':<10} | {'Wildcard Any (::)':<18} | CRITICAL (Overly Permissive)")

        print(f"\n[*] USB Rule Audit Complete. Identified {findings} potential peripheral policy risk(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{rules_path}' not found.")
    except Exception as e:
        print(f"[-] USB policy audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit USBGuard rules for unauthorized mass storage or wildcard access")
    parser.add_argument("-r", "--rules", required=True, type=Path, help="Path to USBGuard rules.conf or policy file")

    args = parser.parse_args()
    audit_usb_rules(args.rules)