import subprocess
import json
import sys
import argparse

def get_network_interfaces() -> None:
    """Audit network interface configurations using cross-platform system calls."""
    print("[+] Gathering active local network interface parameters...\n")

    try:
        if sys.platform.startswith("win32"):
            # Windows PowerShell interface retrieval
            cmd = ["powershell", "-Command", "Get-NetIPInterface | Select-Object InterfaceAlias, AddressFamily, ConnectionState | ConvertTo-Json"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            interfaces = json.loads(result.stdout)
            
            print(f"{'Interface Alias':<25} | {'Family':<10} | {'State'}")
            print("-" * 55)
            for item in interfaces:
                alias = str(item.get("InterfaceAlias", "N/A"))[:24]
                family = "IPv4" if item.get("AddressFamily") == 2 else "IPv6"
                state = "Connected" if item.get("ConnectionState") == 1 else "Disconnected"
                print(f"{alias:<25} | {family:<10} | {state}")

        else:
            # Linux / macOS ip route / addr call
            cmd = ["ip", "-j", "addr"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            interfaces = json.loads(result.stdout)

            print(f"{'Interface':<15} | {'State':<10} | {'MTU':<8} | {'Flags'}")
            print("-" * 60)
            for iface in interfaces:
                ifname = iface.get("ifname", "unknown")
                operstate = iface.get("operstate", "UNKNOWN")
                mtu = iface.get("mtu", 0)
                flags = ",".join(iface.get("flags", []))[:25]
                print(f"{ifname:<15} | {operstate:<10} | {mtu:<8} | {flags}")

    except Exception as e:
        print(f"[-] Unable to query network interface configuration: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit active host network interface states and properties")
    parser.parse_args()
    get_network_interfaces()