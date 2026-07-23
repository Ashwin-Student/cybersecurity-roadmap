import socket
import ssl
from datetime import datetime, timezone
import argparse

def check_ssl_expiry(hostname: str, port: int = 443, warning_days: int = 30) -> None:
    """Connect to an SSL/TLS service and check certificate expiration date."""
    context = ssl.create_default_context()
    
    try:
        # Create TCP connection and wrap with TLS
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        # Parse 'notAfter' date from certificate
        date_fmt = "%b %d %H:%M:%S %Y %Z"
        expires_at = datetime.strptime(cert['notAfter'], date_fmt).replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        
        days_remaining = (expires_at - now).days

        print(f"\n[+] Target: {hostname}:{port}")
        print(f"    Issuer: {dict(x[0] for x in cert['issuer']).get('organizationName', 'Unknown')}")
        print(f"    Expires On: {expires_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"    Days Remaining: {days_remaining}")

        if days_remaining <= 0:
            print("    [!] CRITICAL: Certificate has ALREADY EXPIRED!")
        elif days_remaining <= warning_days:
            print(f"    [!] WARNING: Certificate expires in under {warning_days} days!")
        else:
            print("    [*] STATUS: Certificate is valid.")

    except socket.timeout:
        print(f"[-] Connection to {hostname}:{port} timed out.")
    except ssl.SSLError as e:
        print(f"[-] SSL verification failed for {hostname}: {e}")
    except Exception as e:
        print(f"[-] Error querying {hostname}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSL Certificate Expiry Auditor")
    parser.add_argument("hosts", nargs="+", help="List of hostnames to check (e.g., example.com)")
    parser.add_argument("--days", type=int, default=30, help="Warning threshold in days (default: 30)")
    
    args = parser.parse_args()
    for host in args.hosts:
        check_ssl_expiry(host, warning_days=args.days)