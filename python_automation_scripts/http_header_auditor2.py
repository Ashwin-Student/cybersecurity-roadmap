import urllib.request
import urllib.error
import argparse
import ssl

RECOMMENDED_HEADERS = {
    "Strict-Transport-Security": "Enforces HTTPS connections and protects against downgrade attacks.",
    "Content-Security-Policy": "Restricts sources from which resources (scripts/images) can be loaded.",
    "X-Frame-Options": "Protects against clickjacking by restricting framing.",
    "X-Content-Type-Options": "Prevents MIME-sniffing attacks (should be 'nosniff').",
    "Referrer-Policy": "Controls how much referrer information is included with requests.",
    "Permissions-Policy": "Restricts browser features like camera, microphone, and geolocation."
}

def audit_headers(url: str) -> None:
    """Fetch HTTP headers from a URL and cross-reference against defensive standards."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"[+] Auditing HTTP Security Headers for: {url}\n")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # Allow self-signed during inspection

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SecurityHeaderAuditor/1.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
            headers = {k.title(): v for k, v in response.headers.items()}

        present_count = 0
        missing_count = 0

        for header, description in RECOMMENDED_HEADERS.items():
            header_title = header.title()
            if header_title in headers:
                present_count += 1
                print(f"  [PASS] {header:<28} : {headers[header_title][:40]}")
            else:
                missing_count += 1
                print(f"  [MISSING] {header:<25} : {description}")

        print(f"\n--- Posture Score ---")
        print(f"Configured Headers: {present_count}/{len(RECOMMENDED_HEADERS)}")
        print(f"Missing Hardening:  {missing_count}/{len(RECOMMENDED_HEADERS)}")

    except urllib.error.URLError as e:
        print(f"[-] Connection failed to {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit HTTP Security Hardening Headers on Web Endpoints")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., https://example.com)")

    args = parser.parse_args()
    audit_headers(args.url)