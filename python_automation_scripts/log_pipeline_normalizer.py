import json
import argparse
from pathlib import Path
from typing import Dict, Any

# Field normalization mapping table (Target Field -> Potential Input Keys)
FIELD_MAPPING = {
    "source_ip": ["src", "src_ip", "client_ip", "src_address", "c_ip"],
    "destination_ip": ["dst", "dst_ip", "server_ip", "dest_address", "s_ip"],
    "user_name": ["user", "username", "usr", "account_name", "user_id"],
    "event_action": ["action", "event_type", "activity", "verb"]
}

def normalize_log_entry(raw_record: Dict[str, Any]) -> Dict[str, Any]:
    """Map dynamic log fields into a unified schema."""
    normalized = {"raw_payload": raw_record}

    for standard_key, candidate_keys in FIELD_MAPPING.items():
        for key in candidate_keys:
            if key in raw_record and raw_record[key]:
                normalized[standard_key] = raw_record[key]
                break
        if standard_key not in normalized:
            normalized[standard_key] = None

    return normalized

def process_log_stream(input_file: Path, output_file: Path) -> None:
    """Read un-normalized JSON log lines and write normalized schema objects."""
    print(f"[+] Processing raw log stream from: {input_file}")
    processed_count = 0

    try:
        with open(input_file, "r", encoding="utf-8") as infile, \
             open(output_file, "w", encoding="utf-8") as outfile:

            for line in infile:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    raw_record = json.loads(line)
                    normalized_record = normalize_log_entry(raw_record)
                    outfile.write(json.dumps(normalized_record) + "\n")
                    processed_count += 1
                except json.JSONDecodeError:
                    continue

        print(f"[+] Pipeline Processing Complete. Standardized {processed_count} log records.")
        print(f"[+] Output Written To: {output_file}")

    except FileNotFoundError:
        print(f"[-] Error: File '{input_file}' not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize diverse JSON log streams to a standard field schema")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Path to un-normalized JSON log stream")
    parser.add_argument("-o", "--output", default=Path("normalized_logs.json"), type=Path, help="Normalized output file path")

    args = parser.parse_args()
    process_log_stream(args.input, args.output)