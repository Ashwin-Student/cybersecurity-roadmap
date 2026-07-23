import json
import argparse
from pathlib import Path

DANGEROUS_VERBS = {"*", "create", "update", "patch", "delete", "impersonate"}
CRITICAL_RESOURCES = {"*", "secrets", "pods/exec", "clusterroles", "clusterrolebindings"}

def audit_k8s_rbac(manifest_path: Path) -> None:
    """Inspect K8s RBAC JSON/YAML export for dangerous wildcard permissions."""
    print(f"[+] Auditing Kubernetes RBAC manifest: {manifest_path}\n")

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        rules = data.get("rules", [])
        kind = data.get("kind", "UnknownKind")
        metadata = data.get("metadata", {})
        name = metadata.get("name", "unnamed")

        print(f"Target Resource: {kind}/{name}")
        print(f"{'Rule #':<8} | {'Risk Level':<10} | {'Details'}")
        print("-" * 70)

        findings = 0
        for idx, rule in enumerate(rules, 1):
            verbs = set(rule.get("verbs", []))
            resources = set(rule.get("resources", []))

            has_wildcard_verb = "*" in verbs
            has_wildcard_res = "*" in resources
            has_critical_res = bool(resources.intersection(CRITICAL_RESOURCES))
            has_dangerous_verb = bool(verbs.intersection(DANGEROUS_VERBS))

            if has_wildcard_verb and has_wildcard_res:
                findings += 1
                print(f"{idx:<8} | {'CRITICAL':<10} | Full cluster-admin equivalence (wildcard verbs + wildcard resources).")
            elif has_critical_res and has_dangerous_verb:
                findings += 1
                matched_res = list(resources.intersection(CRITICAL_RESOURCES))
                print(f"{idx:<8} | {'HIGH':<10} | Dangerous access granted to sensitive resource(s): {matched_res}")

        print(f"\n[*] RBAC Audit Complete. Identified {findings} potential over-privilege issue(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{manifest_path}' not found.")
    except Exception as e:
        print(f"[-] RBAC audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Kubernetes ClusterRole definitions for risky privileges")
    parser.add_argument("-m", "--manifest", required=True, type=Path, help="Path to JSON formatted K8s Role/ClusterRole")

    args = parser.parse_args()
    audit_k8s_rbac(args.manifest)
    