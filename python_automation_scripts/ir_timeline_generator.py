import json
import csv
import argparse
from datetime import datetime
from pathlib import Path

def parse_iso_timestamp(ts_str: str) -> datetime:
    """Attempt to parse timestamps into standard datetime objects."""
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%b %d %H:%M:%S"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(ts_str, fmt)
        except ValueError:
            pass
    # Fallback to current time if parsing fails
    return datetime.utcnow()

def generate_timeline(input_json: Path, output_csv: Path) -> None:
    """Import unstructured JSON events, sort chronologically, and output a CSV timeline."""
    print(f"[+] Loading event evidence from: {input_json}")

    try:
        with open(input_json, "r", encoding="utf-8") as f:
            events = json.load(f)

        parsed_events = []
        for item in events:
            raw_ts = item.get("timestamp", "")
            dt_obj = parse_iso_timestamp(raw_ts)

            parsed_events.append({
                "datetime": dt_obj,
                "timestamp_str": dt_obj.strftime("%Y-%m-%d %H:%M:%S"),
                "source_host": item.get("host", "Unknown"),
                "artifact_type": item.get("artifact", "General Log"),
                "description": item.get("description", "")
            })

        # Sort chronologically by datetime
        parsed_events.sort(key=lambda x: x["datetime"])

        # Write to timeline CSV
        with open(output_csv, "w", newline="", encoding="utf-8") as out:
            writer = csv.writer(out)
            writer.writerow(["Timestamp (UTC)", "Host", "Artifact Source", "Event Details"])

            for event in parsed_events:
                writer.writerow([
                    event["timestamp_str"],
                    event["source_host"],
                    event["artifact_type"],
                    event["description"]
                ])

        print(f"[+] Successfully generated timeline with {len(parsed_events)} events.")
        print(f"[+] Saved Incident Response Timeline to: {output_csv}")

    except FileNotFoundError:
        print(f"[-] Input file '{input_json}' not found.")
    except Exception as e:
        print(f"[-] Timeline generation failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consolidate JSON IR events into a sorted forensic timeline")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Input JSON file with events")
    parser.add_argument("-o", "--output", default=Path("ir_timeline.csv"), type=Path, help="Output timeline CSV file")

    args = parser.parse_args()
    generate_timeline(args.input, args.output)
    