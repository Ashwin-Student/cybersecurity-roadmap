import json
import argparse
from collections import Counter
from pathlib import Path

def inspect_waf_logs(log_path: Path, rate_threshold: int) -> None:
    """Analyze WAF log events to flag IPs exceeding request rate thresholds."""
    print(f"[+] Inspecting WAF access logs: {log_path}\n")

    try:
        ip_counter = Counter()
        blocked_counter = Counter()

        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                client_ip = record.get("client_ip", "0.0.0.0")
                action = record.get("action", "ALLOW").upper()

                ip_counter[client_ip] += 1
                if action == "BLOCK":
                    blocked_counter[client_ip] += 1

        print(f"{'Client IP':<20} | {'Total Requests':<15} | {'Blocked Requests':<18} | {'Status'}")
        print("-" * 75)

        flagged_ips = 0
        for ip, count in ip_counter.most_common():
            blocks = blocked_counter.get(ip, 0)
            if count >= rate_threshold:
                flagged_ips += 1
                status = "RATE LIMIT EXCEEDED"
            else:
                status = "NORMAL"

            print(f"{ip:<20} | {count:<15} | {blocks:<18} | {status}")

        print(f"\n[*] Analysis Complete. Identified {flagged_ips} IP address(es) exceeding limit of {rate_threshold} requests.")

    except FileNotFoundError:
        print(f"[-] Error: File '{log_path}' not found.")
    except Exception as e:
        print(f"[-] Log inspection failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect WAF JSON logs for anomalous request spikes")
    parser.add_argument("-l", "--logs", required=True, type=Path, help="Path to WAF JSON log file")
    parser.add_argument("-t", "--threshold", type=int, default=500, help="Request count threshold for flagging (default: 500)")

    args = parser.parse_args()
    inspect_waf_logs(args.logs, args.threshold)