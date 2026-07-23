import argparse
from collections import defaultdict
from pathlib import Path

try:
    from scapy.all import rdpcap, IP, TCP, UDP
except ImportError:
    raise SystemExit("[-] Missing dependency! Install via: pip install scapy")

def analyze_pcap_flows(pcap_path: Path) -> None:
    """Analyze host bandwidth and flow statistics from a PCAP file."""
    print(f"[+] Parsing network packet capture: {pcap_path}")

    try:
        packets = rdpcap(str(pcap_path))
    except Exception as e:
        print(f"[-] Failed to load PCAP file: {e}")
        return

    host_bytes_sent = defaultdict(int)
    conversations = defaultdict(int)

    for pkt in packets:
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            pkt_len = len(pkt)

            host_bytes_sent[src_ip] += pkt_len
            
            # Transport layer port tracking
            proto = "OTHER"
            sport, dport = 0, 0
            if TCP in pkt:
                proto = "TCP"
                sport, dport = pkt[TCP].sport, pkt[TCP].dport
            elif UDP in pkt:
                proto = "UDP"
                sport, dport = pkt[UDP].sport, pkt[UDP].dport

            flow_key = f"{src_ip}:{sport} -> {dst_ip}:{dport} ({proto})"
            conversations[flow_key] += pkt_len

    print(f"\n--- Network Summary ---")
    print(f"Total Packets Processed: {len(packets)}")
    print(f"Unique Active Hosts:     {len(host_bytes_sent)}")

    print("\n--- Top Data Exporters (Bytes Transferred) ---")
    sorted_hosts = sorted(host_bytes_sent.items(), key=lambda x: x[1], reverse=True)
    for ip, bytes_transferred in sorted_hosts[:5]:
        mb = bytes_transferred / (1024 * 1024)
        print(f"  Host {ip:<18} : {mb:.2f} MB ({bytes_transferred} bytes)")

    print("\n--- Top Conversations ---")
    sorted_flows = sorted(conversations.items(), key=lambda x: x[1], reverse=True)
    for flow, bytes_transferred in sorted_flows[:5]:
        kb = bytes_transferred / 1024
        print(f"  {flow:<45} : {kb:.2f} KB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze bandwidth and flow metrics from a PCAP file")
    parser.add_argument("-p", "--pcap", required=True, type=Path, help="Path to .pcap or .pcapng file")

    args = parser.parse_args()
    analyze_pcap_flows(args.pcap)