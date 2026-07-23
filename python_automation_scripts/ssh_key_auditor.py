import os
import stat
import argparse
from pathlib import Path

def audit_ssh_permissions(target_dir: Path) -> None:
    """Scan directory recursively for SSH key files and verify permission compliance."""
    print(f"[+] Scanning for SSH artifacts in: {target_dir}\n")

    ssh_keys_found = 0
    misconfigured_keys = 0

    for root, _, files in os.walk(target_dir):
        for file_name in files:
            # Common SSH key patterns
            if "id_rsa" in file_name or "id_ed25519" in file_name or "id_ecdsa" in file_name:
                file_path = Path(root) / file_name
                
                # Exclude public keys (.pub)
                if file_path.suffix == ".pub":
                    continue

                ssh_keys_found += 1
                try:
                    file_stat = file_path.stat()
                    file_mode = oct(file_stat.st_mode & 0o777)
                    
                    # Permissions strictly required: Owner Read/Write only (0600)
                    is_group_readable = bool(file_stat.st_mode & (stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP))
                    is_world_readable = bool(file_stat.st_mode & (stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH))

                    if is_group_readable or is_world_readable:
                        misconfigured_keys += 1
                        print(f"[!] INSECURE KEY: {file_path}")
                        print(f"    Current Mode: {file_mode} (Should be 0600)")
                        print("    Recommendation: Run 'chmod 600 <file>' to restrict permissions.")
                    else:
                        print(f"[+] SECURE KEY:   {file_path} (Mode: {file_mode})")

                except PermissionError:
                    print(f"[-] Permission denied reading file stats: {file_path}")

    print(f"\n--- Summary ---")
    print(f"Total Private Keys Found: {ssh_keys_found}")
    print(f"Misconfigured Keys:      {misconfigured_keys}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit SSH key directory permissions")
    parser.add_argument("-d", "--dir", type=Path, default=Path.home(), help="Directory to scan (default: Home directory)")
    
    args = parser.parse_args()
    audit_ssh_permissions(args.dir)