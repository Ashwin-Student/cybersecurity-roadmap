import socket
import argparse

DEFAULT_PORTS = [21, 22, 25, 80, 110, 143, 443]

def grab_banner(host: str, port: int, timeout: float = 3.0) -> None:
    """Connect to a host:port and read initial banner sent by the service."""
    try:
        # Create TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))

            # Send a basic trigger for HTTP/HTTPS ports to solicit a banner
            if port in [80, 443]:
                s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")

            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
            
            if banner:
                # Format multiline banners cleanly
                clean_banner = banner.split("\n")[0]
                print(f"  [+] Port {port:<5} OPEN | Banner: {clean_banner[:80]}")
            else:
                print(f"  [+] Port {port:<5} OPEN | (No banner returned)")

    except socket.timeout:
        print(f"  [-] Port {port:<5} Connection timed out.")
    except ConnectionRefusedError:
        print(f"  [-] Port {port:<5} Closed (Connection refused).")
    except Exception as e:
        print(f"  [-] Port {port:<5} Error: {e}")

def main(host: str, ports: list) -> None:
    print(f"\n[+] Starting Banner Grab on Target: {host}")
    for port in ports:
        grab_banner(host, port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Socket Banner Grabber")
    parser.add_argument("host", help="Target hostname or IP address")
    parser.add_argument("-p", "--ports", nargs="+", type=int, default=DEFAULT_PORTS, help="List of ports to scan")

    args = parser.parse_args()
    main(args.host, args.ports)