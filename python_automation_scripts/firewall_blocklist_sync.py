import argparse
from pathlib import Path

def generate_firewall_rules(ioc_file: Path, target_vendor: str) -> None:
    """Generate vendor-specific CLI block commands from an IP IOC text file."""
    print(f"[+] Ingesting IP blocklist from: {ioc_file}")
    
    try:
        with open(ioc_file, "r", encoding="utf-8") as f:
            ips = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        print(f"[+] Total Malicious IPs Ingested: {len(ips)}")
        print(f"[+] Target Syntax Vendor: {target_vendor.upper()}\n")

        print("--- Generated CLI Commands ---")
        for ip in ips:
            if target_vendor.lower() == "paloalto":
                print(f"set address-group static SOC_BLOCKLIST value {ip}")
            elif target_vendor.lower() == "cisco":
                print(f"object-group network SOC_BLOCKLIST host {ip}")
            elif target_vendor.lower() == "fortinet":
                print(f"config firewall address\n  edit \"Block-{ip}\"\n    set subnet {ip} 255.255.255.255\n  next\nend")
            else:
                print(f"iptables -A INPUT -s {ip} -j DROP")

    except FileNotFoundError:
        print(f"[-] Error: File '{ioc_file}' not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate firewall blocklist push commands from IP IOC feeds")
    parser.add_argument("-i", "--iocs", required=True, type=Path, help="Text file containing IP addresses (one per line)")
    parser.add_argument("-v", "--vendor", choices=["paloalto", "cisco", "fortinet", "iptables"], default="iptables", help="Target firewall vendor format")

    args = parser.parse_args()
    generate_firewall_rules(args.iocs, args.vendor)
    