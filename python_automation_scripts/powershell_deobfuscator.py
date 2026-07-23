import re
import base64
import argparse
from pathlib import Path

SUSPICIOUS_KEYWORDS = [
    r"-encodedcommand", r"-enc", r"iex", r"invoke-expression",
    r"downloadstring", r"downloadfile", r"-windowstyle\s+hidden",
    r"bypass", r"-nop", r"-noni"
]

def analyze_powershell(script_path: Path) -> None:
    """Scan PowerShell script for common obfuscation techniques and encoded payloads."""
    print(f"[+] Inspecting PowerShell script: {script_path}\n")

    try:
        with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        findings = 0
        content_lower = content.lower()

        # Check for suspicious keywords
        for pattern in SUSPICIOUS_KEYWORDS:
            matches = re.findall(pattern, content_lower)
            if matches:
                print(f"  [!] Suspicious Keyword Found: '{matches[0]}' (Count: {len(matches)})")
                findings += 1

        # Locate Base64 blocks
        b64_pattern = re.compile(r'(?:[A-Za-z0-9+/]{4}){10,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')
        b64_matches = b64_pattern.findall(content)

        if b64_matches:
            print(f"\n[+] Detected {len(b64_matches)} potential Base64 payload block(s):")
            for idx, block in enumerate(b64_matches[:3], 1):  # Show first 3 matches
                print(f"    Sample {idx}: {block[:40]}...")
                try:
                    decoded = base64.b64decode(block).decode("utf-16le", errors="ignore")
                    if any(kw in decoded.lower() for kw in ["http", "powershell", "cmd"]):
                        print(f"      [!] Decoded Decrypted UTF-16 String: {decoded[:80]}...")
                except Exception:
                    pass

        print(f"\n--- Static Analysis Summary ---")
        print(f"Risk Score: {'HIGH' if findings >= 2 or b64_matches else 'LOW'}")
        print(f"Total Flags Identified: {findings}")

    except FileNotFoundError:
        print(f"[-] Error: File '{script_path}' not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Static PowerShell script obfuscation and risk linter")
    parser.add_argument("-s", "--script", required=True, type=Path, help="Path to target .ps1 script")

    args = parser.parse_args()
    analyze_powershell(args.script)