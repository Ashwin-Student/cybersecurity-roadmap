import argparse
import json
import urllib.request
import urllib.error

def check_ip_reputation(ip_address: str, api_key: str) -> None:
    """Query AbuseIPDB API v2 to retrieve risk scores and report history for an IP."""
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip_address}&maxAgeInDays=90"
    
    headers = {
        "Accept": "application/json",
        "Key": api_key
    }
    
    req = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            data = res_data.get("data", {})

            ip = data.get("ipAddress", ip_address)
            abuse_score = data.get("abuseConfidenceScore", 0)
            country = data.get("countryCode", "Unknown")
            isp = data.get("isp", "Unknown")
            total_reports = data.get("totalReports", 0)

            print(f"\n--- Threat Intel Report for {ip} ---")
            print(f"Country:               {country}")
            print(f"ISP:                   {isp}")
            print(f"Abuse Confidence Score:{abuse_score}%")
            print(f"Total Reports (90d):   {total_reports}")

            if abuse_score > 50:
                print("  [!] ALERT: High probability of malicious activity!")
            elif abuse_score > 20:
                print("  [*] WARNING: Suspicious activity logged.")
            else:
                print("  [+] STATUS: Clean / Low risk profile.")

    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("[-] Unauthorized: Check your API key.")
        else:
            print(f"[-] HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"[-] Connection Error: {e.reason}")
    except Exception as e:
        print(f"[-] Unexpected Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Threat Intel for IP Reputation")
    parser.add_argument("-i", "--ip", required=True, help="Target IP address to check")
    parser.add_argument("-k", "--key", required=True, help="AbuseIPDB API Key")
    
    args = parser.parse_args()
    check_ip_reputation(args.ip, args.key)