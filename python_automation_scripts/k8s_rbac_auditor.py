import yaml
import argparse
from pathlib import Path

HIGH_RISK_VERBS = {"*", "create", "delete", "exec", "bind"}
CRITICAL_RESOURCES = {"secrets", "pods/exec", "serviceaccounts", "clusterroles"}

def audit_k8s_rbac(yaml_path: Path) -> None:
    """Audit Kubernetes Role and ClusterRole definitions for risky API permissions."""
    print(f"[+] Loading Kubernetes Manifest: {yaml_path}\n")

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            docs = list(yaml.safe_load_all(f))

        total_violations = 0

        for doc in docs:
            if not isinstance(doc, dict):
                continue

            kind = doc.get("kind", "")
            metadata = doc.get("metadata", {})
            name = metadata.get("name", "Unnamed")

            if kind in ("Role", "ClusterRole"):
                print(f"--- Auditing {kind}: {name} ---")
                rules = doc.get("rules", [])

                for idx, rule in enumerate(rules, 1):
                    verbs = set(rule.get("verbs", []))
                    resources = set(rule.get("resources", []))

                    risky_verbs = verbs.intersection(HIGH_RISK_VERBS)
                    risky_resources = resources.intersection(CRITICAL_RESOURCES)

                    if "*" in verbs or (risky_verbs and risky_resources):
                        total_violations += 1
                        print(f"  [!] Violation in Rule #{idx}:")
                        print(f"      Resources : {list(resources)}")
                        print(f"      Verbs     : {list(verbs)}")
                        print(f"      Risk      : Excessive control over sensitive resources.\n")

        print(f"[*] Audit Complete. Total High-Risk RBAC Bindings: {total_violations}")

    except FileNotFoundError:
        print(f"[-] Error: File '{yaml_path}' not found.")
    except Exception as e:
        print(f"[-] Failed to parse Kubernetes manifest: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Kubernetes Role/ClusterRole YAML manifests for RBAC risks")
    parser.add_argument("-m", "--manifest", required=True, type=Path, help="Path to Kubernetes RBAC YAML manifest")

    args = parser.parse_args()
    audit_k8s_rbac(args.manifest)