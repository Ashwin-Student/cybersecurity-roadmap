import os
import sys
import argparse

# Recommended CIS Benchmark Kernel Settings
RECOMMENDED_SETTINGS = {
    "/proc/sys/net/ipv4/ip_forward": ("0", "Disable IP Forwarding (Prevents routing between interfaces)"),
    "/proc/sys/net/ipv4/tcp_syncookies": ("1", "Enable SYN Flood Protection"),
    "/proc/sys/net/ipv4/conf/all/accept_redirects": ("0", "Disable ICMP Redirect Acceptance"),
    "/proc/sys/kernel/randomize_va_space": ("2", "Enable Full Address Space Layout Randomization (ASLR)")
}

def audit_sysctl_parameters() -> None:
    """Audit local system kernel runtime variables against security baselines."""
    if not sys.platform.startswith("linux"):
        print("[-] This compliance script requires a Linux kernel environment.")
        return

    print("--- Linux Kernel Security Parameter Audit ---\n")
    print(f"{'Parameter':<45} | {'Current':<8} | {'Expected':<8} | {'Status'}")
    print("-" * 75)

    passed = 0
    failed = 0

    for proc_path, (expected_val, description) in RECOMMENDED_SETTINGS.items():
        param_name = proc_path.replace("/proc/sys/", "").replace("/", ".")
        
        if os.path.exists(proc_path):
            try:
                with open(proc_path, "r") as f:
                    current_val = f.read().strip()

                if current_val == expected_val:
                    status = "PASS"
                    passed += 1
                else:
                    status = "FAIL [!]"
                    failed += 1

                print(f"{param_name:<45} | {current_val:<8} | {expected_val:<8} | {status}")

            except PermissionError:
                print(f"{param_name:<45} | ACCESS DENIED (Run as root)")
        else:
            print(f"{param_name:<45} | NOT FOUND")

    print(f"\n[*] Audit Complete: {passed} Passed, {failed} Failed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Linux kernel security parameters (sysctl)")
    args = parser.parse_args()
    audit_sysctl_parameters()