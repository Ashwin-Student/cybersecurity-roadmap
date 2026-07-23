import json
import hashlib
import argparse
from pathlib import Path

def compute_sha256(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a target file."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()

def create_baseline(target_dir: Path, output_manifest: Path) -> None:
    """Create a baseline JSON manifest of file SHA-256 hashes."""
    print(f"[+] Creating baseline manifest for directory: {target_dir}")
    manifest = {}

    for file_path in target_dir.rglob("*"):
        if file_path.is_file():
            rel_path = str(file_path.relative_to(target_dir))
            manifest[rel_path] = compute_sha256(file_path)

    with open(output_manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[+] Saved baseline with {len(manifest)} file hashes to: {output_manifest}")

def verify_baseline(target_dir: Path, baseline_manifest: Path) -> None:
    """Verify target directory against an existing baseline manifest."""
    print(f"[+] Verifying integrity of: {target_dir} against {baseline_manifest}\n")

    with open(baseline_manifest, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    current_files = {}
    for file_path in target_dir.rglob("*"):
        if file_path.is_file():
            rel_path = str(file_path.relative_to(target_dir))
            current_files[rel_path] = compute_sha256(file_path)

    modified = []
    added = []
    missing = []

    for rel_path, expected_hash in baseline.items():
        if rel_path not in current_files:
            missing.append(rel_path)
        elif current_files[rel_path] != expected_hash:
            modified.append(rel_path)

    for rel_path in current_files:
        if rel_path not in baseline:
            added.append(rel_path)

    print(f"  [!] Modified Files: {len(modified)}")
    for f in modified:
        print(f"      - {f}")

    print(f"  [+] Added Files:    {len(added)}")
    for f in added:
        print(f"      - {f}")

    print(f"  [-] Missing Files:  {len(missing)}")
    for f in missing:
        print(f"      - {f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Baseline and verify directory file integrity using SHA-256")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    create_p = subparsers.add_parser("create")
    create_p.add_argument("-d", "--dir", required=True, type=Path, help="Directory to index")
    create_p.add_argument("-o", "--output", required=True, type=Path, help="Output JSON baseline path")

    verify_p = subparsers.add_parser("verify")
    verify_p.add_argument("-d", "--dir", required=True, type=Path, help="Directory to verify")
    verify_p.add_argument("-b", "--baseline", required=True, type=Path, help="Baseline JSON path")

    args = parser.parse_args()
    if args.mode == "create":
        create_baseline(args.dir, args.output)
    elif args.mode == "verify":
        verify_baseline(args.dir, args.baseline)