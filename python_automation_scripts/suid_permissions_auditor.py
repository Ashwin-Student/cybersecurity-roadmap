import os
import stat
import argparse
from pathlib import Path

def audit_suid_binaries(target_dir: Path, baseline_file: Path = None) -> None:
    """Find SUID/SGID binaries and flag unexpected privileged executables."""
    print(f"[+] Scanning for SUID/SGID executables in: {target_dir}\n")

    baseline = set()
    if baseline_file and baseline_file.is_file():
        with open(baseline_file, "r", encoding="utf-8") as f:
            baseline = {line.strip() for line in f if line.strip() and not line.startswith("#")}

    found_suid = []

    for root, _, files in os.walk(target_dir):
        for file in files:
            file_path = Path(root) / file
            try:
                st = file_path.stat(follow_symlinks=False)
                mode = st.st_mode

                is_suid = bool(mode & stat.S_ISUID)
                is_sgid = bool(mode & stat.S_ISGID)

                if is_suid or is_sgid:
                    path_str = str(file_path)
                    flag_type = "SUID" if is_suid else "SGID"
                    if is_suid and is_sgid:
                        flag_type = "SUID/SGID"

                    is_unapproved = baseline and path_str not in baseline
                    found_suid.append((path_str, flag_type, is_unapproved))

            except (PermissionError, OSError):
                continue

    print(f"{'Binary Path':<50} | {'Permission Flag':<15} | {'Baseline Status'}")
    print("-" * 80)

    unexpected_count = 0
    for path, flag_type, unapproved in found_suid:
        status = "UNAPPROVED [!]" if unapproved else "APPROVED"
        if unapproved:
            unexpected_count += 1
        print(f"{path:<50} | {flag_type:<15} | {status}")

    print(f"\n[*] SUID/SGID Scan Complete. Identified {len(found_suid)} privileged binary(ies) ({unexpected_count} unapproved).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan directories for SUID/SGID binaries and audit against an approved baseline")
    parser.add_argument("-d", "--dir", required=True, type=Path, help="Directory path to scan (e.g., /usr/bin)")
    parser.add_argument("-b", "--baseline", type=Path, help="Optional text file listing approved SUID binary paths")

    args = parser.parse_args()
    audit_suid_binaries(args.dir, args.baseline)