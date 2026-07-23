import json
import argparse
from datetime import datetime
from pathlib import Path

def build_incident_ticket(alert_json: Path, output_file: Path) -> None:
    """Transform alert data into a structured ITSM ticket payload."""
    print(f"[+] Reading alert context from: {alert_json}")

    try:
        with open(alert_json, "r", encoding="utf-8") as f:
            alert = json.load(f)

        incident_id = alert.get("id", "INC-UNASSIGNED")
        severity = alert.get("severity", "MEDIUM").upper()
        title = alert.get("title", "Unclassified Security Event")
        description = alert.get("description", "No detailed context provided.")
        affected_host = alert.get("host", "Unknown Host")
        indicators = alert.get("iocs", [])

        # Format markdown body for the ticket
        markdown_body = (
            f"## Incident Summary: {title}\n\n"
            f"**Generated At:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            f"**Severity Level:** `{severity}`\n"
            f"**Impacted Asset:** `{affected_host}`\n\n"
            f"### Description\n{description}\n\n"
            f"### Extracted Indicators of Compromise (IOCs)\n"
        )

        if indicators:
            for ioc in indicators:
                markdown_body += f"- `{ioc}`\n"
        else:
            markdown_body += "_No explicit IOCs associated with this alert._\n"

        ticket_payload = {
            "ticket_id": f"SOC-{incident_id}",
            "priority": severity,
            "summary": f"[{severity}] {title} on {affected_host}",
            "description_markdown": markdown_body,
            "tags": ["SOC", "Security-Incident", severity.lower()]
        }

        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(ticket_payload, out, indent=4)

        print(f"[+] Formatted ITSM ticket successfully created: {output_file}")

    except FileNotFoundError:
        print(f"[-] Error: File '{alert_json}' not found.")
    except Exception as e:
        print(f"[-] Ticket generation failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate standardized ITSM ticket payload from security alert")
    parser.add_argument("-a", "--alert", required=True, type=Path, help="Path to input alert JSON")
    parser.add_argument("-o", "--output", default=Path("itsm_ticket.json"), type=Path, help="Output JSON ticket path")

    args = parser.parse_args()
    build_incident_ticket(args.alert, args.output)