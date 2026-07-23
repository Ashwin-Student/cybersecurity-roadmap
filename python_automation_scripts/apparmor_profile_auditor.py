import argparse
from pathlib import Path

def audit_apparmor_profiles(profiles_dir: Path) -> None:
    """Inspect AppArmor profile files for enforce vs complain mode flags."""
    print(f"[+] Inspecting AppArmor profile definitions in: {profiles_dir}\n")

    if not profiles_dir.is_dir():
        print(f"[-] Error: Directory '{profiles_dir}' does not exist.")
        return

    enforce_count = 0
    complain_count = 0

    print(f"{'Profile Name':<45} | {'Mode'}")
    print("-" * 60)

    for profile_file in profiles_dir.glob("*"):
        if profile_file.is_file():
            try:
                with open(profile_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # AppArmor profiles contain 'flags=(complain)' when in permissive mode
                if "flags=(complain)" in content or "flags=(attach_disconnected,complain)" in content:
                    mode = "COMPLAIN (Permissive)"
                    complain_count += 1
                else:
                    mode = "ENFORCE (Active)"
                    enforce_count += 1

                print(f"{profile_file.name:<45} | {mode}")

            except Exception as e:
                print(f"[-] Failed to read {profile_file.name}: {e}")

    print(f"\n[*] AppArmor Summary: {enforce_count} Enforcing, {complain_count} Complain mode profile(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit AppArmor profile definitions for enforcement modes")
    parser.add_argument("-d", "--dir", required=True, type=Path, help="Path to AppArmor profiles directory (e.g., /etc/apparmor.d)")

    args = parser.parse_args()
    audit_apparmor_profiles(args.dir)