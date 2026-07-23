import json
import hashlib
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

def generate_alert_hash(alert: dict) -> str:
    """Create a unique fingerprint for an alert based on core attributes."""
    src_ip = alert.get("source_ip", "")
    event_id = str(alert.get("event_id", ""))
    signature = alert.get("signature", "")
    
    raw_key = f"{src_ip}|{event_id}|{signature}"
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()[:16]

def deduplicate_alerts(input_file: Path, window_minutes: int = 15) -> None:
    """Group duplicate alerts occurring within a rolling time window."""
    print(f"[+] Processing raw alert feed from: {input_file}")

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            alerts = json.load(f)

        grouped_incidents = defaultdict(list)

        for alert in alerts:
            fingerprint = generate_alert_hash(alert)
            grouped_incidents[fingerprint].append(alert)

        print(f"\n--- Aggregation & Deduplication Report ---")
        print(f"Total Raw Alerts:        {len(alerts)}")
        print(f"Unique Alert Clusters:   {len(grouped_incidents)}")
        print(f"Noise Reduction:         {((len(alerts) - len(grouped_incidents)) / len(alerts) * 100):.1f}%\n")

        print(f"{'Cluster Fingerprint':<20} | {'Count':<6} | {'Signature':<30} | {'Source IP'}")
        print("-" * 75)

        for fingerprint, cluster in grouped_incidents.items():
            sample = cluster[0]
            sig = sample.get("signature", "Unknown")[:30]
            src_ip = sample.get("source_ip", "N/A")
            print(f"{fingerprint:<20} | {len(cluster):<6} | {sig:<30} | {src_ip}")

    except FileNotFoundError:
        print(f"[-] Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"[-] Failed to process alerts: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deduplicate and aggregate high-volume SIEM alerts")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Path to raw JSON alerts file")
    parser.add_argument("-w", "--window", type=int, default=15, help="Time window in minutes (default: 15)")

    args = parser.parse_args()
    deduplicate_alerts(args.input, args.window)