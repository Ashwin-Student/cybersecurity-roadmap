import argparse
from collections import defaultdict
try:
    from scapy.all import rdpcap, IP
except ImportError:
    raise SystemExit("[-] Missing dependency! Install scapy via: pip install scapy")

def format_bytes(size_bytes: int) -> str:
    """Format bytes into readable units (KB, MB, GB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def calculate_bandwidth(pcap_path: str) -> None:
    """Parse PCAP to summarize byte counts sent and received per IP."""
    print(f"[+] Processing PCAP capture: {pcap_path} ...")

    try:
        packets = rdpcap(pcap_path)
    except FileNotFoundError:
        print(f"[-] Error: File not found at '{pcap_path}'")
        return
    except Exception as e:
        print(f"[-] Error reading PCAP file: {e}")
        return

    sent_bytes = defaultdict(int)
    received_bytes = defaultdict(int)
    total_volume = 0

    for pkt in packets:
        if pkt.haslayer(IP):
            pkt_len = len(pkt)
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst

            sent_bytes[src_ip] += pkt_len
            received_bytes[dst_ip] += pkt_len
            total_volume += pkt_len

    all_ips = set(sent_bytes.keys()).union(set(received_bytes.keys()))

    print(f"\n--- PCAP Bandwidth Summary ---")
    print(f"Total Network Capture Volume: {format_bytes(total_volume)}\n")
    print(f"{'IP Address':<18} | {'Sent Data':<12} | {'Received Data':<12}")
    print("-" * 48)

    # Sort by total combined volume descending
    sorted_ips = sorted(all_ips, key=lambda ip: sent_bytes[ip] + received_bytes[ip], reverse=True)

    for ip in sorted_ips[:10]:  # Show top 10 bandwidth consumers
        sent = format_bytes(sent_bytes[ip])
        recv = format_bytes(received_bytes[ip])
        print(f"{ip:<18} | {sent:<12} | {recv:<12}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate network bandwidth utilization per IP from PCAP")
    parser.add_argument("-f", "--file", required=True, help="Path to input .pcap file")
    
    args = parser.parse_args()
    calculate_bandwidth(args.file)