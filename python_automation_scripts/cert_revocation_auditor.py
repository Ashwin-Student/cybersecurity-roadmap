import json
import argparse
from pathlib import Path

def audit_cert_revocation_endpoints(cert_metadata_path: Path) -> None:
    """Check parsed certificate records for valid CRL and OCSP endpoint configurations."""
    print(f"[+] Auditing Certificate Revocation metadata: {cert_metadata_path}\n")

    try:
        with open(cert_metadata_path, "r", encoding="utf-8") as f:
            certificates = json.load(f)

        findings = 0
        print(f"{'Subject Domain':<25} | {'CRL Defined':<12} | {'OCSP Defined':<12} | {'Status'}")
        print("-" * 75)

        for cert in certificates:
            domain = cert.get("subject_domain", "unknown")[:24]
            crl_urls = cert.get("crl_distribution_points", [])
            ocsp_urls = cert.get("ocsp_responders", [])

            has_crl = len(crl_urls) > 0
            has_ocsp = len(ocsp_urls) > 0

            if not has_crl and not has_ocsp:
                status = "CRITICAL (No Revocation Method)"
                findings += 1
            elif not has_ocsp:
                status = "WARN (Missing OCSP Stapling)"
                findings += 1
            else:
                status = "PASS"

            crl_str = "Yes" if has_crl else "No"
            ocsp_str = "Yes" if has_ocsp else "No"

            print(f"{domain:<25} | {crl_str:<12} | {ocsp_str:<12} | {status}")

        print(f"\n[*] Audit Complete. Identified {findings} certificate configuration gap(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{cert_metadata_path}' not found.")
    except Exception as e:
        print(f"[-] Certificate revocation audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit parsed X.509 certificate records for CRL and OCSP URLs")
    parser.add_argument("-m", "--metadata", required=True, type=Path, help="Path to certificate metadata JSON")

    args = parser.parse_args()
    audit_cert_revocation_endpoints(args.metadata)