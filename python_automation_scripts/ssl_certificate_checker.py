import socket
import ssl
import datetime
import argparse
from typing import Optional, Dict

def check_ssl_certificate(hostname: str, port: int = 443) -> Optional[Dict]:
    """Retrieve SSL certificate metadata for a remote endpoint."""
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Parse expiration date
                not_after_str = cert.get("notAfter")
                expiry_date = datetime.datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %GMT")
                days_left = (expiry_date - datetime.datetime.utcnow()).days

                # Extract Issuer Common Name
                issuer = dict(x[0] for x in cert.get("issuer", ()))
                issuer_name = issuer.get("commonName", "Unknown Issuer")

                return {
                    "hostname": hostname,
                    "expiry_date": expiry_date.strftime("%Y-%m-%d"),
                    "days_remaining": days_left,
                    "issuer": issuer_name
                }
    except Exception as e:
        print(f"[-] Failed to establish SSL context with {hostname}:{port} -> {e}")
        return None

def audit_certificates(targets: list, warning_threshold: int) -> None:
    """Inspect list of domain names and issue alerts for expiring certs."""
    print(f"[+] Beginning SSL/TLS Certificate Audit across {len(targets)} host(s)\n")
    print(f"{'Target Host':<25} | {'Expiry Date':<12} | {'Days Left':<10} | {'Issuer'}")
    print("-" * 75)

    for host in targets:
        host = host.strip()
        if not host:
            continue

        result = check_ssl_certificate(host)
        if result:
            days = result["days_remaining"]
            alert_prefix = ""

            if days <= 0:
                alert_prefix = "[EXPIRED] "
            elif days <= warning_threshold:
                alert_prefix = "[WARNING] "

            print(
                f"{alert_prefix + result['hostname']:<25} | "
                f"{result['expiry_date']:<12} | "
                f"{days:<10} | "
                f"{result['issuer']}"
            )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit remote HTTPS servers for TLS certificate validity")
    parser.add_argument("-t", "--targets", nargs="+", required=True, help="List of hostnames or domain names to check")
    parser.add_argument("-w", "--warning-days", type=int, default=30, help="Days threshold for expiry warning alert")

    args = parser.parse_args()
    audit_certificates(args.targets, args.warning_days)