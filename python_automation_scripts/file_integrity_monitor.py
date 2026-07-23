import argparse
import json
import hashlib
from pathlib import Path

def calculate_sha256(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a file reading in chunks to handle large files."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Read in 64KB blocks
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (PermissionError, FileNotFoundError):
        return ""

def generate_baseline(directory: Path, baseline_file: Path) -> None:
    """Scan target directory and save current state to a JSON file."""
    print(f"[+] Generating baseline for: {directory}")
    baseline = {}
    
    for file_path in directory.rglob("*"):
        if file_path.is_file() and file_path != baseline_file:
            rel_path = str(file_path.relative_to(directory))
            baseline[rel_path] = calculate_sha256(file_path)

    with open(baseline_file, "w") as f:
        json.dump(baseline, f, indent=4)
    print(f"[+] Baseline stored successfully at: {baseline_file}")

def verify_integrity(directory: Path, baseline_file: Path) -> None:
    """Compare current directory state against saved baseline."""
    if not baseline_file.exists():
        print("[-] Baseline file not found! Run with --mode build first.")
        return

    with open(baseline_file, "r") as f:
        baseline = json.load(f)

    current_files = {}
    for file_path in directory.rglob("*"):
        if file_path.is_file() and file_path != baseline_file:
            rel_path = str(file_path.relative_to(directory))
            current_files[rel_path] = calculate_sha256(file_path)

    print(f"\n--- Integrity Audit Results for {directory} ---")
    
    # Check modified or missing files
    for path, original_hash in baseline.items():
        if path not in current_files:
            print(f"[DELETED] File missing: {path}")
        elif current_files[path] != original_hash:
            print(f"[MODIFIED] Hash mismatch: {path}")

    # Check for newly added files
    for path in current_files:
        if path not in baseline:
            print(f"[ADDED] New file detected: {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple File Integrity Monitor")
    parser.add_argument("-d", "--dir", required=True, type=Path, help="Target directory to scan")
    parser.add_argument("-b", "--baseline", default=Path("baseline.json"), type=Path, help="Path for baseline JSON storage")
    parser.add_argument("-m", "--mode", choices=["build", "check"], required=True, help="Mode: build baseline or check integrity")
    
    args = parser.parse_args()

    if args.mode == "build":
        generate_baseline(args.dir, args.baseline)
    elif args.mode == "check":
        verify_integrity(args.dir, args.baseline)