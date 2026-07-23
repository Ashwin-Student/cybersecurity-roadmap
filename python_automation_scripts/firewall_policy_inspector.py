import argparse
try:
    import psutil
except ImportError:
    raise SystemExit("[-] Missing dependency! Install psutil via: pip install psutil")

def inspect_listening_ports() -> None:
    """Enumerate open listening sockets and associate them with running processes."""
    print("--- Open Listening Sockets Audit ---\n")
    print(f"{'Proto':<6} | {'Local Address':<22} | {'PID':<6} | {'Process Name':<20}")
    print("-" * 62)

    listening_count = 0

    try:
        connections = psutil.net_connections(kind="inet")
        for conn in connections:
            if conn.status == psutil.CONN_LISTEN:
                listening_count += 1
                proto = "TCP" if conn.type == 1 else "UDP"
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
                pid = conn.pid or "N/A"

                # Retrieve process name
                proc_name = "Unknown"
                if conn.pid:
                    try:
                        proc_name = psutil.Process(conn.pid).name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        proc_name = "Access Denied"

                print(f"{proto:<6} | {laddr:<22} | {str(pid):<6} | {proc_name:<20}")

        print(f"\n[*] Total Open Listening Ports: {listening_count}")

    except psutil.AccessDenied:
        print("[-] Permission Denied: Run with administrative privileges for full process mappings.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit local listening ports and bound processes")
    args = parser.parse_args()
    inspect_listening_ports()