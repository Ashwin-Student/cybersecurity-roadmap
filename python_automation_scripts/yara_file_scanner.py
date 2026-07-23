import argparse
from pathlib import Path
try:
    import yara
except ImportError:
    raise SystemExit("[-] Missing dependency! Please install yara-python: pip install yara-python")

def scan_target_with_yara(rules_path: Path, target_path: Path) -> None:
    """Compile YARA rules and scan a target directory or file."""
    print(f"[+] Compiling YARA rule file: {rules_path}")
    try:
        rules = yara.compile(filepath=str(rules_path))
    except yara.SyntaxError as e:
        print(f"[-] YARA Rule Syntax Error: {e}")
        return
    except Exception as e:
        print(f"[-] Failed to load rules: {e}")
        return

    print(f"[+] Scanning target: {target_path}\n")

    files_to_scan = []
    if target_path.is_file():
        files_to_scan.append(target_path)
    elif target_path.is_dir():
        files_to_scan = [p for p in target_path.rglob("*") if p.is_file()]

    matches_found = 0
    for file_p in files_to_scan:
        try:
            matches = rules.match(str(file_p))
            if matches:
                matches_found += 1
                match_names = ", ".join([m.rule for m in matches])
                print(f"  [!] YARA MATCH: {file_p}")
                print(f"      Matched Rules: {match_names}")
        except yara.Error as e:
            print(f"  [-] Error scanning {file_p}: {e}")

    print(f"\n--- YARA Audit Complete ---")
    print(f"Total Matches Identified: {matches_found}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan local files using YARA rules")
    parser.add_argument("-r", "--rules", required=True, type=Path, help="Path to compiled or raw .yar YARA rule file")
    parser.add_argument("-t", "--target", required=True, type=Path, help="Target file or directory to scan")

    args = parser.parse_args()
    scan_target_with_yara(args.rules, args.target)