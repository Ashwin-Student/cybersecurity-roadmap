import re
import argparse
from pathlib import Path

# Regular expressions for IOC extraction
IOC_PATTERNS = {
    "IPv4 Address": re.compile(rb"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"),
    "URL": re.compile(rb"https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?:/[^\s]*)?"),
    "Email Address": re.compile(rb"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
}

def extract_iocs_from_dump(dump_path: Path, min_len: int = 4) -> None:
    """Scan memory dump binary stream for forensic IOC indicators."""
    print(f"[+] Scanning memory dump for forensic indicators: {dump_path}\n")

    try:
        with open(dump_path, "rb") as f:
            content = f.read()

        print("--- Forensic Extracted Indicators ---")
        for ioc_type, pattern in IOC_PATTERNS.items():
            matches = set(pattern.findall(content))
            print(f"\n[>] {ioc_type} Matches ({len(matches)} found):")
            for m in list(matches)[:10]:  # Show first 10 unique
                try:
                    print(f"  - {m.decode('utf-8', errors='ignore')}")
                except Exception:
                    pass

    except FileNotFoundError:
        print(f"[-] Error: File '{dump_path}' not found.")
    except Exception as e:
        print(f"[-] Extraction failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract network IOC strings from binary memory dumps")
    parser.add_argument("-d", "--dump", required=True, type=Path, help="Path to raw memory dump file")

    args = parser.parse_args()
    extract_iocs_from_dump(args.dump)