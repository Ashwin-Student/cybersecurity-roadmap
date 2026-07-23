import subprocess
import sys
import argparse

def isolate_host(trusted_management_ip: str) -> None:
    """Apply strict iptables firewall rules to isolate the machine on the network."""
    if not sys.platform.startswith("linux"):
        print("[-] Host isolation via iptables requires a Linux OS.")
        return

    print(f"[!] INITIATING EMERGENCY HOST ISOLATION PROCEDURE [!]")
    print(f"[+] Preserving outbound connectivity to management/SIEM IP: {trusted_management_ip}\n")

    # Commands sequence to lock down the interface
    commands = [
        # Flush existing rules
        ["iptables", "-F"],
        ["iptables", "-X"],

        # Allow local loopback traffic
        ["iptables", "-A", "INPUT", "-i", "lo", "-j", "ACCEPT"],
        ["iptables", "-A", "OUTPUT", "-o", "lo", "-j", "ACCEPT"],

        # Allow established SOC/Management connections
        ["iptables", "-A", "INPUT", "-s", trusted_management_ip, "-j", "ACCEPT"],
        ["iptables", "-A", "OUTPUT", "-d", trusted_management_ip, "-j", "ACCEPT"],

        # Drop all other traffic
        ["iptables", "-P", "INPUT", "DROP"],
        ["iptables", "-P", "FORWARD", "DROP"],
        ["iptables", "-P", "OUTPUT", "DROP"]
    ]

    try:
        for cmd in commands:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("[+] Firewall rules updated successfully. Host is now isolated.")
    except PermissionError:
        print("[-] Execution failed: Root privileges (sudo) required.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to execute isolation step: {e.stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Isolate compromised Linux host leaving only management access")
    parser.add_argument("-m", "--mgmt-ip", required=True, help="Trusted Security/SIEM Server IP to remain accessible")

    args = parser.parse_args()
    isolate_host(args.mgmt-ip)