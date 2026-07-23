import urllib.request
import argparse
import ssl

SECURITY_HEADERS = {
    "Strict-Transport-Security": "Enforces HTTPS connections (HSTS).",
    "Content-Security-Policy": "Mitigates XSS and data injection attacks.",
    "X-Frame-Options": "Protects against Clickjacking.",
    "X-Content-Type-Options": "Prevents MIME-sniffing vulnerabilities.",
    "Referrer-Policy": "Controls how much referrer information is sent."
}

def audit_headers(url: str) -> None:
    """Fetch HTTP response headers and flag missing security configurations."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"[+] Auditing headers for: {url}\n")
    
    # Ignore SSL errors for local test targets if necessary
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "SecAuditBot/1.0"}
    )

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            headers = dict(response.info())

            found_count = 0
            for header_name, description in SECURITY_HEADERS.items():
                # Case-insensitive header matching
                matched_val = next((v for k, v in headers.items() if k.lower() == header_name.lower()), None)

                if matched_val:
                    print(f"[PRESENT] {header_name}: {matched_val}")
                    found_count += 1
                else:
                    print(f"[MISSING] {header_name} - {description}")

            score = (found_count / len(SECURITY_HEADERS)) * 100
            print(f"\n[*] Compliance Score: {score:.0f}% ({found_count}/{len(SECURITY_HEADERS)} headers present)")

    except Exception as e:
        print(f"[-] Request failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit HTTP Security Headers")
    parser.add_argument("url", help="Target URL (e.g., https://example.com)")
    args = parser.parse_args()

    audit_headers(args.url)