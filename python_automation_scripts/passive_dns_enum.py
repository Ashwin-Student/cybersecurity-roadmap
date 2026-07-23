import json
import urllib.request
import argparse
from pathlib import Path

def query_passive_dns(domain: str, output_path: Path = None) -> None:
    """Query passive DNS endpoint for historical resolution data."""
    print(f"[+] Querying passive DNS records for domain: {domain}\n")
    
    # Using HackerTarget public passive DNS API endpoint
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SecOps-ThreatIntel/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode("utf-8")

        if "error" in data.lower() or not data.strip():
            print("[-] No passive DNS results found or API rate limit reached.")
            return

        records = [line.split(",") for line in data.strip().split("\n") if "," in line]

        print(f"{'Subdomain / Hostname':<40} | {'IP Address'}")
        print("-" * 65)

        for host, ip in records:
            print(f"{host:<40} | {ip}")

        print(f"\n[*] Discovered {len(records)} historical DNS mapping(s).")

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump([{"hostname": h, "ip": i} for h, i in records], f, indent=2)
            print(f"[+] Results saved to: {output_path}")

    except Exception as e:
        print(f"[-] Passive DNS query failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enumerate historical passive DNS records and subdomains")
    parser.add_argument("-d", "--domain", required=True, help="Target root domain (e.g., example.com)")
    parser.add_argument("-o", "--output", type=Path, help="Optional output JSON path")

    args = parser.parse_args()
    query_passive_dns(args.domain, args.output)