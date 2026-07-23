import argparse
from pathlib import Path

BACKUP_EXTENSIONS = {".sql", ".bak", ".dump", ".tar", ".gz"}
ENCRYPTED_EXTENSIONS = {".gpg", ".enc", ".age", ".aes"}

def audit_backup_directory(target_dir: Path) -> None:
    """Identify unencrypted database backup files on disk."""
    print(f"[+] Scanning directory for unencrypted database backups: {target_dir}\n")

    if not target_dir.is_dir():
        print(f"[-] Error: Directory '{target_dir}' does not exist.")
        return

    unencrypted_files = []

    for file_path in target_dir.rglob("*"):
        if file_path.is_file():
            exts = [e.lower() for e in file_path.suffixes]

            # Check if file looks like a backup
            is_backup = any(ext in BACKUP_EXTENSIONS for ext in exts)
            # Check if file has an encryption extension wrapper
            is_encrypted = any(ext in ENCRYPTED_EXTENSIONS for ext in exts)

            if is_backup and not is_encrypted:
                size_mb = round(file_path.stat().st_size / (1024 * 1024), 2)
                unencrypted_files.append((file_path, size_mb))

    if unencrypted_files:
        print(f"{'File Path':<50} | {'Size (MB)'}")
        print("-" * 65)
        for path, size in unencrypted_files:
            print(f"{str(path):<50} | {size}")
        print(f"\n[CRITICAL] Found {len(unencrypted_files)} unencrypted backup file(s) stored on disk.")
    else:
        print("[PASS] No unencrypted backup files detected in target directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan target directory for plain-text unencrypted database dump files")
    parser.add_argument("-d", "--dir", required=True, type=Path, help="Directory path to scan")

    args = parser.parse_args()
    audit_backup_directory(args.dir)