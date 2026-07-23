import json
import argparse
from pathlib import Path

def convert_json_to_csv_archive(json_file: Path, output_csv: Path) -> None:
    """Extract flat log fields and write to CSV archive format (Parquet precursor)."""
    print(f"[+] Reading JSON log file: {json_file}")

    try:
        records = []
        with open(json_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))

        if not records:
            print("[-] No valid JSON records found.")
            return

        # Extract unified headers
        headers = list({key for record in records for key in record.keys()})

        import csv
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for record in records:
                writer.writerow(record)

        print(f"[+] Data Lake Archival File Successfully Created: {output_csv}")
        print(f"    Total Processed Events: {len(records)}")

    except FileNotFoundError:
        print(f"[-] Error: File '{json_file}' not found.")
    except Exception as e:
        print(f"[-] Processing failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSON log lines into structured Data Lake CSV/Archival format")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Path to input JSON log file")
    parser.add_argument("-o", "--output", default=Path("security_archive.csv"), type=Path, help="Path for structured output archive")

    args = parser.parse_args()
    convert_json_to_csv_archive(args.input, args.output)