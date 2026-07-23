import hashlib
import json
import argparse
from pathlib import Path

def compute_sha256(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a given file in chunks."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except PermissionError:
        return "PERMISSION_DENIED"
    except FileNotFoundError:
        return "FILE_NOT_FOUND"

def create_baseline(target_dir: Path, baseline_file: Path) -> None:
    """Generate a SHA-256 snapshot mapping for all files in a directory."""
    print(f"[+] Creating file integrity baseline for directory: {target_dir}")
    baseline = {}

    for file_p in target_dir.rglob("*"):
        if file_p.is_file() and file_p != baseline_file:
            rel_path = str(file_p.relative_to(target_dir))
            baseline[rel_path] = compute_sha256(file_p)

    with open(baseline_file, "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=4)

    print(f"[+] Baseline saved with {len(baseline)} monitored files to '{baseline_file}'")

def verify_integrity(target_dir: Path, baseline_file: Path) -> None:
    """Compare current directory state against saved SHA-256 baseline."""
    if not baseline_file.exists():
        print(f"[-] Error: Baseline file '{baseline_file}' does not exist.")
        return

    print(f"[+] Auditing directory integrity using baseline: {baseline_file}\n")
    with open(baseline_file, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    current_files = set()
    modified_count = 0
    created_count = 0

    for file_p in target_dir.rglob("*"):
        if file_p.is_file() and file_p != baseline_file:
            rel_path = str(file_p.relative_to(target_dir))
            current_files.add(rel_path)

            current_hash = compute_sha256(file_p)
            expected_hash = baseline.get(rel_path)

            if expected_hash is None:
                print(f"  [+] NEW FILE DETECTED: {rel_path}")
                created_count += 1
            elif current_hash != expected_hash:
                print(f"  [!] FILE MODIFIED: {rel_path}")
                modified_count += 1

    # Check for deleted files
    deleted_count = 0
    for rel_path in baseline.keys():
        if rel_path not in current_files:
            print(f"  [-] FILE DELETED: {rel_path}")
            deleted_count += 1

    print("\n--- Integrity Report ---")
    print(f"Modified: {modified_count} | Created: {created_count} | Deleted: {deleted_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Host File Integrity Monitor (FIM)")
    parser.add_argument("-d", "--dir", required=True, type=Path, help="Target directory to monitor")
    parser.add_argument("-b", "--baseline", default=Path("fim_baseline.json"), type=Path, help="Baseline storage file")
    parser.add_argument("--mode", choices=["create", "verify"], required=True, help="Mode: create baseline or verify integrity")

    args = parser.parse_args()
    if args.mode == "create":
        create_baseline(args.dir, args.baseline)
    else:
        verify_integrity(args.dir, args.baseline)