import re
import argparse
from pathlib import Path

REQUIRED_META = {"author", "description", "severity"}

def audit_yara_rule(rule_path: Path) -> None:
    """Inspect YARA rule text for syntax best practices and metadata completeness."""
    print(f"[+] Auditing YARA detection rule: {rule_path}\n")

    try:
        with open(rule_path, "r", encoding="utf-8") as f:
            content = f.read()

        findings = 0
        rule_names = re.findall(r'rule\s+([A-Za-z0-9_]+)', content)
        print(f"[*] Detected Rules: {', '.join(rule_names) if rule_names else 'None'}\n")

        # Check meta block presence
        if "meta:" not in content:
            findings += 1
            print("  [HIGH] Rule is missing a 'meta:' metadata block.")
        else:
            meta_block = content.split("meta:")[1].split("strings:")[0] if "strings:" in content else content.split("meta:")[1]
            for field in REQUIRED_META:
                if field not in meta_block.lower():
                    findings += 1
                    print(f"  [WARN] Missing recommended metadata key: '{field}'")

        # Check for overly broad or short strings
        strings_match = re.search(r'strings:\s*(.*?)\s*condition:', content, re.DOTALL)
        if strings_match:
            strings_block = strings_match.group(1)
            for line in strings_block.strip().splitlines():
                line_str = line.strip()
                # Flag short hex strings (e.g., {$ 90 90 $})
                if "= {" in line_str and len(line_str.split("{")[1].split("}")[0].strip().split()) < 4:
                    findings += 1
                    print(f"  [WARN] Short hex string detected (potential false positive risk): {line_str}")

        print(f"\n[*] YARA Audit Complete. Found {findings} rule quality warning(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{rule_path}' not found.")
    except Exception as e:
        print(f"[-] YARA rule audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit YARA rule files for metadata standards and pattern quality")
    parser.add_argument("-r", "--rule", required=True, type=Path, help="Path to .yar or .yara rule file")

    args = parser.parse_args()
    audit_yara_rule(args.rule)