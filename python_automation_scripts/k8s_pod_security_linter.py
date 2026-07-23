import json
import argparse
from pathlib import Path

def lint_pod_spec(pod_manifest: Path) -> None:
    """Audit Pod specification for secure runtime securityContext flags."""
    print(f"[+] Linting Pod Security Context: {pod_manifest}\n")

    try:
        with open(pod_manifest, "r", encoding="utf-8") as f:
            data = json.load(f)

        containers = data.get("spec", {}).get("containers", [])
        findings = 0

        for container in containers:
            c_name = container.get("name", "unknown")
            sec_ctx = container.get("securityContext", {})

            run_as_non_root = sec_ctx.get("runAsNonRoot", False)
            read_only_root = sec_ctx.get("readOnlyRootFilesystem", False)
            allow_priv_esc = sec_ctx.get("allowPrivilegeEscalation", True)
            privileged = sec_ctx.get("privileged", False)

            print(f"Checking Container: '{c_name}'")

            if privileged:
                findings += 1
                print("  [CRITICAL] Container is configured with 'privileged: true'!")

            if not run_as_non_root:
                findings += 1
                print("  [HIGH] 'runAsNonRoot' is missing or set to false.")

            if allow_priv_esc:
                findings += 1
                print("  [MEDIUM] 'allowPrivilegeEscalation' should be explicitly set to false.")

            if not read_only_root:
                findings += 1
                print("  [LOW] Root filesystem is mutable ('readOnlyRootFilesystem' is false).")

        print(f"\n[*] Pod Security Audit Complete. Found {findings} security gap(s).")

    except FileNotFoundError:
        print(f"[-] Error: File '{pod_manifest}' not found.")
    except Exception as e:
        print(f"[-] Pod security linting failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Kubernetes Pod securityContext settings")
    parser.add_argument("-p", "--pod", required=True, type=Path, help="Path to Pod manifest JSON")

    args = parser.parse_args()
    lint_pod_spec(args.pod)
    