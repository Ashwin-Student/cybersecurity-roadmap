import json
import argparse
from pathlib import Path
from collections import defaultdict

SENSITIVE_EVENTS = {
    "CreateUser", "AttachUserPolicy", "PutBucketPolicy", 
    "StopLogging", "DeleteTrail", "AuthorizeSecurityGroupIngress"
}

def analyze_cloudtrail(trail_file: Path) -> None:
    """Parse CloudTrail JSON events and flag high-risk sensitive API invocations."""
    print(f"[+] Ingesting CloudTrail logs from: {trail_file}\n")

    user_event_counts = defaultdict(lambda: defaultdict(int))
    sensitive_findings = []

    try:
        with open(trail_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        records = data.get("Records", [])

        for record in records:
            event_name = record.get("eventName", "Unknown")
            user_identity = record.get("userIdentity", {}).get("userName", "UnknownUser")
            event_time = record.get("eventTime", "N/A")

            user_event_counts[user_identity][event_name] += 1

            if event_name in SENSITIVE_EVENTS:
                sensitive_findings.append((event_time, user_identity, event_name))

        print(f"--- Processed {len(records)} Total Events ---")
        print(f"\n[!] Sensitive API Invocations Detected ({len(sensitive_findings)}):")
        for time, user, event in sensitive_findings:
            print(f"  [{time}] User: '{user}' executed Sensitive API -> {event}")

    except FileNotFoundError:
        print(f"[-] Error: File '{trail_file}' not found.")
    except Exception as e:
        print(f"[-] Failed to process CloudTrail log: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse AWS CloudTrail JSON logs for sensitive administrative API calls")
    parser.add_argument("-t", "--trail", required=True, type=Path, help="Path to CloudTrail JSON export file")

    args = parser.parse_args()
    analyze_cloudtrail(args.trail)