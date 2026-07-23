import re
import argparse
from collections import Counter
from pathlib import Path

# Common log patterns (matches standard Apache/Nginx combined format)
LOG_PATTERN = re.compile(
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+-\s+-\s+\[(?P<time>[^\]]+)\]\s+"(?P<method>\w+)\s+(?P<url>\S+)\s+HTTP/[0-9\.]+"\s+(?P<status>\d{3})\s+(?P<bytes>\d+|-)'
)

def analyze_access_log(log_path: Path, threshold: int) -> None:
    """Parse web server access log and detect suspicious traffic patterns."""
    ip_counter = Counter()
    status_counter = Counter()
    failed_auth_ips = Counter()

    print(f"[+] Ingesting and parsing log file: {log_path}")

    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = LOG_PATTERN.search(line)
                if match:
                    data = match.groupdict()
                    ip = data["ip"]
                    status = data["status"]

                    ip_counter[ip] += 1
                    status_counter[status] += 1

                    # Track 401 (Unauthorized) or 403 (Forbidden) attempts
                    if status in ("401", "403"):
                        failed_auth_ips[ip] += 1

        print("\n--- Summary Statistics ---")
        print(f"Total Requests Processed: {sum(ip_counter.values())}")
        print(f"Unique Source IPs:        {len(ip_counter)}")

        print("\n--- Top IP Traffic Sources ---")
        for ip, count in ip_counter.most_common(5):
            print(f"  {ip:<18} : {count} requests")

        print("\n[!] Potential Security Anomalies (Requests Exceeding Threshold) [!]")
        anomalies_found = 0
        for ip, count in ip_counter.items():
            if count >= threshold:
                print(f"  [ALERT] High Traffic Volume: {ip:<18} -> {count} requests")
                anomalies_found += 1

        for ip, count in failed_auth_ips.items():
            if count >= 5:
                print(f"  [ALERT] Repeated Auth Failure: {ip:<18} -> {count} failed requests")
                anomalies_found += 1

        if anomalies_found == 0:
            print("  No anomalies detected matching current thresholds.")

    except FileNotFoundError:
        print(f"[-] Error: Log file not found at '{log_path}'")
    except Exception as e:
        print(f"[-] Log analysis failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit access logs for high-volume or anomalous activity")
    parser.add_argument("-l", "--log", required=True, type=Path, help="Path to web server log file")
    parser.add_argument("-t", "--threshold", default=100, type=int, help="Request count threshold for alert trigger")

    args = parser.parse_args()
    analyze_access_log(args.log, args.threshold)