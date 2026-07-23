import csv
import json
import re
import argparse
from pathlib import Path

# Common IOC Validation Regex Patterns
IP_PATTERN = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
DOMAIN_PATTERN = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")
HASH_SHA256_PATTERN = re.compile(r"^[a-fA-F0-9]{64}$")
HASH_MD5_PATTERN = re.compile(r"^[a-fA-F0-9]{32}$")

def categorize_ioc(value: str) -> str:
    """Identify the type of indicator using regular expressions."""
    value = value.strip().replace("[.]", ".") # Handle defanged indicators
    if IP_PATTERN.match(value):
        return "ip_address"
    elif DOMAIN_PATTERN.match(value):
        return "domain"
    elif HASH_SHA256_PATTERN.match(value):
        return "sha256"
    elif HASH_MD5_PATTERN.match(value):
        return "md5"
    return "unknown"

def normalize_csv_feed(csv_path: Path, output_path: Path) -> None:
    """Parse a CSV threat feed and export a standardized JSON IOC object."""
    normalized_data = {
        "metadata": {
            "source_file": csv_path.name,
            "total_records": 0
        },
        "indicators": []
    }

    print(f"[+] Ingesting threat feed from: {csv_path}")
    try:
        with open(csv_path, mode="r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row in reader:
                # Skip header or empty rows
                if not row or row[0].startswith("#"):
                    continue

                for cell in row:
                    cell_clean = cell.strip()
                    ioc_type = categorize_ioc(cell_clean)

                    if ioc_type != "unknown":
                        normalized_data["indicators"].append({
                            "indicator": cell_clean.replace("[.]", "."),
                            "type": ioc_type,
                            "status": "active"
                        })
                        normalized_data["metadata"]["total_records"] += 1

        # Write out standardized JSON structure
        with open(output_path, mode="w", encoding="utf-8") as out:
            json.dump(normalized_data, out, indent=4)

        print(f"[+] Successfully normalized {normalized_data['metadata']['total_records']} indicators.")
        print(f"[+] Standardized feed saved to: {output_path}")

    except FileNotFoundError:
        print(f"[-] Error: Input file not found at '{csv_path}'")
    except Exception as e:
        print(f"[-] Unexpected error during processing: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize CSV Threat Feeds into Standardized JSON")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Input CSV threat feed file")
    parser.add_argument("-o", "--output", default=Path("normalized_iocs.json"), type=Path, help="Output JSON path")

    args = parser.parse_args()
    normalize_csv_feed(args.input, args.output)