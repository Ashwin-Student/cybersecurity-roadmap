import argparse
from collections import Counter
from pathlib import Path

# Mapping of common MITRE ATT&CK Technique IDs to Tactic Domains
ATTACK_TACTIC_MAP = {
    "T1566": "Initial Access",
    "T1190": "Initial Access",
    "T1059": "Execution",
    "T1053": "Execution",
    "T1543": "Persistence",
    "T1078": "Defense Evasion / Initial Access",
    "T1003": "Credential Access",
    "T1021": "Lateral Movement",
    "T1041": "Exfiltration"
}

def generate_attack_heatmap(technique_file: Path) -> None:
    """Aggregate technique IDs from a file and display ATT&CK tactic distribution."""
    print(f"[+] Loading detected technique IDs from: {technique_file}\n")

    tactic_counter = Counter()
    technique_counter = Counter()

    try:
        with open(technique_file, "r", encoding="utf-8") as f:
            for line in f:
                tech_id = line.strip().upper()
                if not tech_id or tech_id.startswith("#"):
                    continue

                technique_counter[tech_id] += 1
                tactic = ATTACK_TACTIC_MAP.get(tech_id, "Unmapped / Other Tactic")
                tactic_counter[tactic] += 1

        print("--- Top Detected MITRE ATT&CK Techniques ---")
        for tech, count in technique_counter.most_common(5):
            print(f"  {tech:<10} : {count} occurrence(s)")

        print("\n--- Coverage Summary by Tactic Category ---")
        for tactic, count in tactic_counter.most_common():
            print(f"  {tactic:<32} : {count} technique(s)")

    except FileNotFoundError:
        print(f"[-] Error: Technique list file '{technique_file}' not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map detected technique IDs to MITRE ATT&CK tactic distribution")
    parser.add_argument("-t", "--techniques", required=True, type=Path, help="Text file with MITRE Technique IDs (one per line)")

    args = parser.parse_args()
    generate_attack_heatmap(args.techniques)