import json
import argparse
from pathlib import Path

SUSPICIOUS_NAMES = {"default", "raspberrypi", "esp32", "test", "admin"}

def lint_ble_devices(scan_file: Path) -> None:
    """Audit BLE device scan data for missing encryption or default identities."""
    print(f"[+] Auditing BLE discovery scan records: {scan_file}\n")

    try:
        with open(scan_file, "r", encoding="utf-8") as f:
            devices = json.load(f)

        findings = 0
        print(f"{'MAC Address':<18} | {'Device Name':<20} | {'RSSI':<8} | {'Security Flags'}")
        print("-" * 75)

        for dev in devices:
            mac = dev.get("address", "00:00:00:00:00:00")
            name = dev.get("name", "Unknown")[:19]
            rssi = dev.get("rssi", -100)
            authenticated = dev.get("authenticated", False)
            encrypted = dev.get("encrypted", False)

            issues = []
            if not encrypted:
                issues.append("Unencrypted Link")
            if not authenticated:
                issues.append("No Authentication")
            if any(susp in name.lower() for susp in SUSPICIOUS_NAMES):
                issues.append("Default/Dev Name")

            if issues:
                findings += 1
                flag_str = ", ".join(issues)
            else:
                flag_str = "SECURE"

            print(f"{mac:<18} | {name:<20} | {rssi:<8} | {flag_str}")

        print(f"\n[*] BLE Scan Audit Complete. Identified {findings} potential wireless device risk(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{scan_file}' not found.")
    except Exception as e:
        print(f"[-] BLE audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Bluetooth Low Energy scan data for encryption and pairing risks")
    parser.add_argument("-s", "--scan", required=True, type=Path, help="Path to BLE discovery JSON file")

    args = parser.parse_args()
    lint_ble_devices(args.scan)