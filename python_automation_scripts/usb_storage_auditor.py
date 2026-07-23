import re
import subprocess
import argparse
from pathlib import Path

# USB Mass Storage kernel log pattern
USB_PATTERN = re.compile(
    r"usb\s+(?P<dev_id>\d+-\d+):\s+New USB device found,\s+idVendor=(?P<vendor>\w+),\s+idProduct=(?P<product>\w+)"
)

def audit_usb_events(log_path: Path = None) -> None:
    """Parse kernel messages for USB mass storage connection events."""
    print("--- Removable Storage (USB) Attachment Audit ---\n")

    log_lines = []
    if log_path and log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                log_lines = f.readlines()
        except Exception as e:
            print(f"[-] Error reading file: {e}")
            return
    else:
        # Fallback to dmesg output
        try:
            res = subprocess.run(["dmesg"], capture_output=True, text=True)
            log_lines = res.stdout.splitlines()
        except Exception as e:
            print(f"[-] System dmesg query failed: {e}")
            return

    usb_events = 0
    print(f"{'Device ID':<12} | {'Vendor ID':<10} | {'Product ID':<10} | {'Raw Log Match'}")
    print("-" * 75)

    for line in log_lines:
        match = USB_PATTERN.search(line)
        if match:
            usb_events += 1
            data = match.groupdict()
            print(f"{data['dev_id']:<12} | {data['vendor']:<10} | {data['product']:<10} | {line.strip()[:30]}...")

    print(f"\n[*] Audit Complete: Detected {usb_events} USB storage connection event(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit system logs for USB storage attachment events")
    parser.add_argument("-l", "--log", type=Path, help="Optional path to syslog file (defaults to live dmesg)")

    args = parser.parse_args()
    audit_usb_events(args.log)