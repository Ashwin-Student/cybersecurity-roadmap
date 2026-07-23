import socket
import ssl
import argparse
from datetime import datetime

def inspect_tls_endpoint(hostname: str, port: int = 443) -> None:
    """Connect to a TLS endpoint and check certificate expiration and active protocol."""
    print(f"[+] Connecting to TLS endpoint: {hostname}:{port}\n")

    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=5.0) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher, version, secret_bits = ssock.cipher()

                # Parse certificate expiration timestamp
                not_after_str = cert.get("notAfter")
                # Example format: 'May 10 23:59:59 2026 GMT'
                expire_date = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
                days_left = (expire_date - datetime.utcnow()).days

                print("--- TLS Certificate & Connection Metrics ---")
                print(f"  Target Hostname:    {hostname}")
                print(f"  TLS Version:        {version}")
                print(f"  Active Cipher:      {cipher} ({secret_bits} bits)")
                print(f"  Expiration Date:    {expire_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")

                if days_left < 0:
                    print(f"  Status:             [CRITICAL] Certificate EXPIRED {abs(days_left)} day(s) ago!")
                elif days_left < 30:
                    print(f"  Status:             [WARNING] Certificate expires soon ({days_left} days remaining)!")
                else:
                    print(f"  Status:             [HEALTHY] Certificate valid for {days_left} more days.")

    except socket.timeout:
        print(f"[-] Connection timed out connecting to {hostname}:{port}")
    except ssl.SSLError as err:
        print(f"[-] SSL/TLS Handshake Error on {hostname}: {err}")
    except Exception as e:
        print(f"[-] Failed to audit target endpoint: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit HTTPS/TLS certificate expiration dates and negotiated cipher parameters")
    parser.add_argument("-t", "--target", required=True, help="Target domain or hostname (e.g., example.com)")
    parser.add_argument("-p", "--port", type=int, default=443, help="TLS port (default: 443)")

    args = parser.parse_args()
    inspect_tls_endpoint(args.target, args.port)