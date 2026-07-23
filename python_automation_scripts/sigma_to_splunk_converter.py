import yaml
import argparse
from pathlib import Path
from typing import Dict, Any

def convert_sigma_to_splunk(sigma_path: Path) -> None:
    """Parse a Sigma rule YAML file and generate a basic Splunk SPL query."""
    print(f"[+] Ingesting Sigma Rule: {sigma_path}\n")

    try:
        with open(sigma_path, "r", encoding="utf-8") as f:
            rule = yaml.safe_load(f)

        title = rule.get("title", "Untitled Rule")
        description = rule.get("description", "No description provided.")
        logsource = rule.get("logsource", {})
        detection = rule.get("detection", {})

        print("--- Rule Metadata ---")
        print(f"Title:       {title}")
        print(f"Description: {description}")
        print(f"Logsource:   {logsource}\n")

        spl_terms = []

        # Map logsource to Splunk index/sourcetype if specified
        if "category" in logsource:
            spl_terms.append(f'category="{logsource["category"]}"')
        if "product" in logsource:
            spl_terms.append(f'product="{logsource["product"]}"')

        # Process detection selections
        for key, value in detection.items():
            if key == "condition":
                continue

            if isinstance(value, dict):
                for field, val in value.items():
                    if isinstance(val, list):
                        formatted_vals = " OR ".join([f'"{v}"' for v in val])
                        spl_terms.append(f"({field} IN ({formatted_vals}))")
                    else:
                        spl_terms.append(f'{field}="{val}"')
            elif isinstance(value, list):
                formatted_vals = " OR ".join([f'"{v}"' for v in value])
                spl_terms.append(f"({formatted_vals})")

        spl_query = "index=* " + " ".join(spl_terms)

        print("--- Generated Splunk SPL Query ---")
        print(f"  {spl_query}\n")

    except FileNotFoundError:
        print(f"[-] Error: File '{sigma_path}' not found.")
    except Exception as e:
        print(f"[-] Failed to process Sigma rule: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert basic Sigma detection rules to Splunk SPL queries")
    parser.add_argument("-r", "--rule", required=True, type=Path, help="Path to Sigma YAML rule file")

    args = parser.parse_args()
    convert_sigma_to_splunk(args.rule)