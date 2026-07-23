import argparse
from pathlib import Path

# Minimum acceptable key lengths
MIN_KEY_SIZES = {
    "RSA": 2048,
    "DSA": 2048,
    "EC": 256
}

DEPRECATED_ALGORITHMS = {"SHA1", "MD5", "MD4", "DES", "3DES", "RC4"}

def lint_pem_key(pem_path: Path) -> None:
    """Inspect text of PEM file to check algorithm declarations and length markers."""
    print(f"[+] Inspecting cryptographic file: {pem_path}\n")

    try:
        with open(pem_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        print("--- Cryptographic Compliance Check ---")
        findings = 0

        # Scan for deprecated algorithm names in plain text headers/descriptors
        for dep_alg in DEPRECATED_ALGORITHMS:
            if dep_alg in content.upper():
                findings += 1
                print(f"  [!] DEPRECATED ALGORITHM DETECTED: {dep_alg}")

        if "-----BEGIN RSA PRIVATE KEY-----" in content:
            print("  [*] Identified Type: RSA Private Key")
            # Primitive check for short legacy key length indicators
            if "Proc-Type: 4,ENCRYPTED" not in content and len(content) < 1200:
                findings += 1
                print("  [!] WARNING: Key length appears shorter than recommended 2048 bits.")

        elif "-----BEGIN CERTIFICATE-----" in content:
            print("  [*] Identified Type: X.509 Certificate")

        if findings == 0:
            print("  [PASS] No obvious deprecated algorithm signatures identified.")
        else:
            print(f"\n[*] Audit Complete with {findings} potential weakness warning(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{pem_path}' not found.")
    except Exception as e:
        print(f"[-] Crypto audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lint PEM files for deprecated cryptographic algorithms or short keys")
    parser.add_argument("-f", "--file", required=True, type=Path, help="Path to PEM certificate or key file")

    args = parser.parse_args()
    lint_pem_key(args.file)