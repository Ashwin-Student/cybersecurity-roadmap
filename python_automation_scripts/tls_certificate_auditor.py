import ssl
import socket
import argparse
from datetime import datetime
from pathlib import Path
from typing import List

def audit_tls_certificate(hostname: str, port: int = 443, warning_days: int = 30) -> None:
    """Connect to a server and audit its SSL/TLS certificate validity and protocol."""
    print(f"[+] Inspecting TLS configuration for: {hostname}:{port}")

    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                protocol = ssock.version()

                # Extract Expiration Date
                not_after_str = cert.get("notAfter", "")
                # Format: 'MMM DD HH:MM:SS YYYY GMT'
                expire_date = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
                days_left = (expire_date - datetime.utcnow()).days

                # Extract Issuer
                issuer = dict(x[0] for x in cert.get("issuer", ()))
                issuer_name = issuer.get("organizationName", "Unknown Issuer")

                print("\n--- TLS Audit Summary ---")
                print(f"  Target Host        : {hostname}")
                print(f"  Negotiated Protocol: {protocol}")
                print(f"  Active Cipher      : {cipher[0]} ({cipher[2]} bits)")
                print(f"  Issuer             : {issuer_name}")
                print(f"  Expiration Date    : {expire_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                print(f"  Days Remaining     : {days_left} day(s)")

                if days_left <= 0:
                    print("  [CRITICAL ALERT] Certificate has ALREADY EXPIRED!")
                elif days_left <= warning_days:
                    print(f"  [WARNING] Certificate expires in less than {warning_days} days!")
                else:
                    print("  [PASS] Certificate status is healthy.")

    except socket.timeout:
        print(f"[-] Connection timeout while reaching {hostname}:{port}")
    except ssl.SSLError as e:
        print(f"[-] SSL/TLS Handshake Error on {hostname}: {e}")
    except Exception as e:
        print(f"[-] Audit failed for {hostname}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit TLS certificate expiration and cipher negotiating for domains")
    parser.add_argument("-d", "--domain", required=True, help="Target domain name or IP (e.g., example.com)")
    parser.add_argument("-p", "--port", type=int, default=443, help="HTTPS port (default: 443)")
    parser.add_argument("-w", "--warning-days", type=int, default=30, help="Days threshold for expiration warning")

    args = parser.parse_args()
    audit_tls_certificate(args.domain, args.port, args.warning_days)