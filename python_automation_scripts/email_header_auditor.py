import argparse
from email import message_from_file
import re

def parse_email_authentication(eml_path: str) -> None:
    """Extract and analyze authentication results from an .eml email file."""
    print(f"[+] Analyzing email headers in: {eml_path}\n")

    try:
        with open(eml_path, "r", encoding="utf-8", errors="ignore") as f:
            msg = message_from_file(f)

        # Extract standard header fields
        from_hdr = msg.get("From", "Unknown")
        return_path = msg.get("Return-Path", "Unknown")
        auth_results = msg.get("Authentication-Results", "Not Present")
        spf_hdr = msg.get("Received-SPF", "Not Present")

        print("--- Sender Metadata ---")
        print(f"From Header: {from_hdr}")
        print(f"Return-Path: {return_path}")

        print("\n--- Authentication Checks ---")
        print(f"SPF Header:             {spf_hdr[:100]}")
        print(f"Authentication Results: {auth_results[:120]}")

        # Basic SPF validation heuristic
        if "pass" in spf_hdr.lower() or "pass" in auth_results.lower():
            print("\n[+] SPF/DKIM Status: PASS")
        elif "fail" in spf_hdr.lower() or "fail" in auth_results.lower():
            print("\n[!] ALERT: SPF/DKIM Validation FAILED! Domain may be spoofed.")
        else:
            print("\n[*] SPF/DKIM Status: Inconclusive / Missing Headers.")

    except FileNotFoundError:
        print(f"[-] Error: File '{eml_path}' not found.")
    except Exception as e:
        print(f"[-] Error parsing email headers: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse email headers for SPF and DKIM authentication results")
    parser.add_argument("-f", "--file", required=True, help="Path to raw .eml file")

    args = parser.parse_args()
    parse_email_authentication(args.file)