import json
import argparse
from datetime import datetime
from pathlib import Path

# SLA thresholds in minutes per severity level
SLA_THRESHOLDS_MINUTES = {
    "CRITICAL": {"ack": 15, "resolve": 60},
    "HIGH":     {"ack": 30, "resolve": 240},
    "MEDIUM":   {"ack": 60, "resolve": 1440},
    "LOW":      {"ack": 240, "resolve": 4320}
}

def audit_incident_slas(incidents_file: Path) -> None:
    """Evaluate active tickets against ACK and Resolution SLA windows."""
    print(f"[+] Ingesting active tickets from: {incidents_file}\n")

    try:
        with open(incidents_file, "r", encoding="utf-8") as f:
            incidents = json.load(f)

        now = datetime.utcnow()
        breached_count = 0

        print(f"{'Ticket ID':<12} | {'Severity':<8} | {'Age (min)':<10} | {'ACK Status':<12} | {'Resolution Status'}")
        print("-" * 75)

        for ticket in incidents:
            tid = ticket.get("id", "UNKNOWN")
            severity = ticket.get("severity", "MEDIUM").upper()
            created_str = ticket.get("created_at")
            acked = ticket.get("acknowledged", False)
            resolved = ticket.get("resolved", False)

            if not created_str:
                continue

            created_dt = datetime.fromisoformat(created_str.replace("Z", ""))
            age_minutes = int((now - created_dt).total_seconds() / 60)

            thresholds = SLA_THRESHOLDS_MINUTES.get(severity, SLA_THRESHOLDS_MINUTES["MEDIUM"])

            # Evaluate Acknowledgement SLA
            ack_status = "ACK'D" if acked else ("BREACHED" if age_minutes > thresholds["ack"] else "PENDING")

            # Evaluate Resolution SLA
            if resolved:
                res_status = "RESOLVED"
            elif age_minutes > thresholds["resolve"]:
                res_status = "BREACHED [!]"
                breached_count += 1
            else:
                res_status = "IN PROGRESS"

            print(f"{tid:<12} | {severity:<8} | {age_minutes:<10} | {ack_status:<12} | {res_status}")

        print(f"\n[*] SLA Audit Summary: {breached_count} ticket(s) currently violating resolution SLA.")

    except FileNotFoundError:
        print(f"[-] Error: File '{incidents_file}' not found.")
    except Exception as e:
        print(f"[-] Failed to process incident metrics: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit active SOC incident tickets for SLA breaches")
    parser.add_argument("-i", "--incidents", required=True, type=Path, help="Path to JSON file with incident tickets")

    args = parser.parse_args()
    audit_incident_slas(args.incidents)