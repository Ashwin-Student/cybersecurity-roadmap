import re
import argparse

def defang_url(text: str) -> str:
    """Sanitize URLs and IPs by neutralizing protocol schemas and domain dots."""
    # Replace http:// and https:// with hxxp:// and hxxps://
    text = re.sub(r"http://", "hxxp://", text, flags=re.IGNORECASE)
    text = re.sub(r"https://", "hxxps://", text, flags=re.IGNORECASE)
    # Neutralize periods in domain names or IP addresses
    text = text.replace(".", "[.]")
    return text

def refang_url(text: str) -> str:
    """Restore defanged indicators back to standard network format."""
    text = re.sub(r"hxxp://", "http://", text, flags=re.IGNORECASE)
    text = re.sub(r"hxxps://", "https://", text, flags=re.IGNORECASE)
    text = text.replace("[.]", ".")
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URL Defanger / Refanger Utility")
    parser.add_argument("target", help="URL or IP string to process")
    parser.add_argument("-m", "--mode", choices=["defang", "refang"], default="defang", help="Operation mode")

    args = parser.parse_args()

    if args.mode == "defang":
        result = defang_url(args.target)
        print(f"\n[+] Defanged Indicator:\n{result}")
    else:
        result = refang_url(args.target)
        print(f"\n[+] Refanged Indicator:\n{result}")