import re
import argparse
from email import message_from_file
from urllib.parse import urlparse
from pathlib import Path

URL_PATTERN = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
SHORTENER_DOMAINS = {"bit.ly", "tinyurl.com", "goo.gl", "is.gd", "buff.ly", "ow.ly", "t.co"}

def analyze_phishing_eml(eml_path: Path) -> None:
    """Parse EML file, extract links, and audit for suspicious characteristics."""
    print(f"[+] Inspecting suspicious email artifact: {eml_path}\n")

    try:
        with open(eml_path, "r", encoding="utf-8", errors="ignore") as f:
            msg = message_from_file(f)

        subject = msg.get("Subject", "No Subject")
        sender = msg.get("From", "Unknown Sender")

        print("--- Email Headers ---")
        print(f"Subject: {subject}")
        print(f"From:    {sender}")

        # Extract email body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() in ("text/plain", "text/html"):
                    body += part.get_payload(decode=True).decode("utf-8", errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

        # Find URLs
        urls = URL_PATTERN.findall(body)
        print(f"\n--- Extracted URLs ({len(urls)} found) ---")

        risk_score = 0
        for url in set(urls):
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            indicators = []
            
            # Check for IP-based URL
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", domain):
                indicators.append("Raw IP Address URL")
                risk_score += 3

            # Check for URL shortener
            if domain in SHORTENER_DOMAINS:
                indicators.append("URL Shortener Detected")
                risk_score += 2

            # Check for suspicious TLD or excessive length
            if len(url) > 100:
                indicators.append("Unusually Long URL")
                risk_score += 1

            status_str = f" | [!] Flags: {', '.join(indicators)}" if indicators else " | Safe/Standard"
            print(f"  -> {url[:70]}...{status_str}")

        print(f"\n--- Assessment Summary ---")
        print(f"Calculated Risk Score: {risk_score}")
        if risk_score >= 4:
            print("[ALERT] High Risk: Email exhibits multiple indicators of a phishing attempt.")
        elif risk_score >= 2:
            print("[WARNING] Medium Risk: Suspicious elements found. Manual review recommended.")
        else:
            print("[INFO] Low Risk: No obvious automated phishing flags identified.")

    except Exception as e:
        print(f"[-] Email parsing failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze .eml email artifacts for phishing indicators and suspicious links")
    parser.add_argument("-e", "--eml", required=True, type=Path, help="Path to raw .eml email file")

    args = parser.parse_args()
    analyze_phishing_eml(args.eml)