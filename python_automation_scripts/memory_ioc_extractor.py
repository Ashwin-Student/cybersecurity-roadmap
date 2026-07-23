import re
import argparse
from pathlib import Path
from typing import Generator

# RegEx patterns for extracted memory strings
IOC_PATTERNS = {
    "IPv4 Address": re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"),
    "URL": re.compile(r"https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?:/[^\s]*)?"),
    "Windows Registry Key": re.compile(r"(?:HKLM|HKCU|HKEY_LOCAL_MACHINE|HKEY_CURRENT_USER)\\[a-zA-Z0-9_\\\-]+", re.IGNORECASE),
    "Executable File Path": re.compile(r"[C-Z]:\\[a-zA-Z0-9_\\\-\s]+\.(?:exe|dll|bat|ps1|vbs)", re.IGNORECASE)
}

def extract_strings_from_file(file_path: Path, min_length: int = 6) -> Generator[str, None, None]:
    """Extract printable ASCII and UTF-16 strings from a raw memory image file."""
    ascii_pattern = re.compile(rb"[\x20-\x7E]{" + str(min_length).encode() + rb",}")
    unicode_pattern = re.compile(rb"(?:[\x20-\x7E]\x00){" + str(min_length).encode() + rb",}")

    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(1024 * 1024):  # Read in 1MB chunks
                for match in ascii_pattern.finditer(chunk):
                    yield match.group().decode("ascii", errors="ignore")
                for match in unicode_pattern.finditer(chunk):
                    yield match.group().decode("utf-16le", errors="ignore")
    except Exception as e:
        print(f"[-] Error reading memory file: {e}")

def audit_memory_dump(dump_path: Path) -> None:
    """Scan extracted memory strings for IOCs."""
    print(f"[+] Ingesting raw memory dump: {dump_path}\n")
    findings = {key: set() for key in IOC_PATTERNS}

    total_strings = 0
    for extracted_str in extract_strings_from_file(dump_path):
        total_strings += 1
        for category, pattern in IOC_PATTERNS.items():
            matches = pattern.findall(extracted_str)
            for m in matches:
                findings[category].add(m)

    print(f"[*] Processed {total_strings} string chunks.")
    print("\n--- Extracted Forensic Indicators ---")

    for category, indicators in findings.items():
        print(f"\n[+] {category} ({len(indicators)} unique):")
        for idx, item in enumerate(sorted(indicators)[:10], 1):  # Display top 10 unique
            print(f"   {idx}. {item}")
        if len(indicators) > 10:
            print(f"   ... and {len(indicators) - 10} more.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract forensic indicators and strings from raw RAM dumps")
    parser.add_argument("-m", "--memory-dump", required=True, type=Path, help="Path to raw memory dump file (.dmp / .raw)")

    args = parser.parse_args()
    audit_memory_dump(args.memory_dump)