import argparse
from collections import Counter
try:
    from scapy.all import rdpcap, IP, TCP, UDP, ICMP
except ImportError:
    raise SystemExit("[-] Missing dependency! Please install scapy: pip install scapy")

def analyze_pcap(file_path: str) -> None:
    """Read a .pcap file and display packet statistics grouped by protocol."""
    print(f"[+] Loading PCAP file: {file_path} ...")
    
    try:
        packets = rdpcap(file_path)
    except FileNotFoundError:
        print(f"[-] Error: PCAP file not found at '{file_path}'")
        return
    except Exception as e:
        print(f"[-] Error parsing PCAP: {e}")
        return

    protocol_counter = Counter()
    ip_sources = Counter()

    for pkt in packets:
        if pkt.haslayer(IP):
            ip_sources[pkt[IP].src] += 1

            if pkt.haslayer(TCP):
                protocol_counter["TCP"] += 1
            elif pkt.haslayer(UDP):
                protocol_counter["UDP"] += 1
            elif pkt.haslayer(ICMP):
                protocol_counter["ICMP"] += 1
            else:
                protocol_counter["Other IP"] += 1
        else:
            protocol_counter["Non-IP"] += 1

    print("\n--- Network Protocol Summary ---")
    print(f"Total Packets Captured: {len(packets)}")
    for proto, count in protocol_counter.items():
        percentage = (count / len(packets)) * 100
        print(f"  {proto:<10}: {count:<6} ({percentage:.1f}%)")

    print("\n--- Top 5 Source IP Addresses ---")
    for ip, count in ip_sources.most_common(5):
        print(f"  {ip:<15}: {count} packets")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze PCAP file protocol statistics")
    parser.add_argument("-f", "--file", required=True, help="Path to input .pcap file")
    
    args = parser.parse_args()
    analyze_pcap(args.file)