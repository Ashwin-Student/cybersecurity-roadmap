import json
import argparse
from pathlib import Path

def audit_sbom(sbom_path: Path) -> None:
    """Parse CycloneDX SBOM JSON file and list tracked dependencies and licenses."""
    print(f"[+] Ingesting Software Bill of Materials (SBOM): {sbom_path}\n")

    try:
        with open(sbom_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        bom_format = data.get("bomFormat", "Unknown")
        components = data.get("components", [])

        print(f"--- SBOM Overview ({bom_format}) ---")
        print(f"Total Components Tracked: {len(components)}\n")

        print(f"{'Component Name':<30} | {'Version':<12} | {'Licenses'}")
        print("-" * 70)

        for comp in components:
            name = comp.get("name", "Unknown")[:30]
            version = comp.get("version", "N/A")[:12]
            
            # Extract license information
            licenses = []
            for lic_entry in comp.get("licenses", []):
                if "license" in lic_entry:
                    licenses.append(lic_entry["license"].get("id") or lic_entry["license"].get("name", ""))
            
            lic_str = ", ".join(licenses) if licenses else "Unspecified"
            print(f"{name:<30} | {version:<12} | {lic_str}")

    except FileNotFoundError:
        print(f"[-] Error: File '{sbom_path}' not found.")
    except Exception as e:
        print(f"[-] Failed to process SBOM file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse CycloneDX SBOM JSON files for dependency governance")
    parser.add_argument("-s", "--sbom", required=True, type=Path, help="Path to CycloneDX JSON SBOM file")

    args = parser.parse_args()
    audit_sbom(args.sbom)