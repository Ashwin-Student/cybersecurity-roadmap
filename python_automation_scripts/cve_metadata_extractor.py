import argparse
import json
import urllib.request
import urllib.error

def fetch_cve_details(cve_id: str) -> None:
    """Fetch vulnerability metadata for a specific CVE from the NVD API."""
    cve_id = cve_id.upper().strip()
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    
    headers = {
        "User-Agent": "Python-Vulnerability-Auditor/1.0"
    }
    
    req = urllib.request.Request(url, headers=headers, method="GET")

    print(f"[+] Querying National Vulnerability Database for: {cve_id} ...")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            vulnerabilities = res_data.get("vulnerabilities", [])

            if not vulnerabilities:
                print(f"[-] No records found for {cve_id}.")
                return

            cve_item = vulnerabilities[0].get("cve", {})
            descriptions = cve_item.get("descriptions", [])
            desc_text = next((d["value"] for d in descriptions if d.get("lang") == "en"), "No description available.")

            # Metrics parsing (CVSS v3.1 primary score)
            metrics = cve_item.get("metrics", {})
            cvss_data = None
            if "cvssMetricV31" in metrics:
                cvss_data = metrics["cvssMetricV31"][0].get("cvssData", {})
            elif "cvssMetricV30" in metrics:
                cvss_data = metrics["cvssMetricV30"][0].get("cvssData", {})

            print(f"\n--- CVE Metadata Report: {cve_id} ---")
            if cvss_data:
                base_score = cvss_data.get("baseScore", "N/A")
                severity = cvss_data.get("baseSeverity", "N/A")
                vector = cvss_data.get("vectorString", "N/A")
                print(f"Base Severity: {severity} ({base_score})")
                print(f"CVSS Vector:   {vector}")
            else:
                print("Base Severity: N/A (CVSS metrics not populated)")

            print(f"\nDescription:\n{desc_text}\n")

    except urllib.error.HTTPError as e:
        print(f"[-] HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"[-] Connection failed: {e.reason}")
    except Exception as e:
        print(f"[-] Unexpected error parsing CVE data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract CVE details from NVD API")
    parser.add_argument("-c", "--cve", required=True, help="CVE ID (e.g., CVE-2021-44228)")
    
    args = parser.parse_args()
    fetch_cve_details(args.cve)