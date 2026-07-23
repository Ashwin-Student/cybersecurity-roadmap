import argparse
from pathlib import Path

def lint_dockerfile(dockerfile_path: Path) -> None:
    """Audit Dockerfile instructions for security best practices."""
    print(f"[+] Inspecting Dockerfile: {dockerfile_path}\n")

    try:
        with open(dockerfile_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        has_user_instruction = False
        has_healthcheck = False
        findings = 0

        print(f"{'Line':<6} | {'Severity':<8} | {'Rule Violation'}")
        print("-" * 75)

        for line_num, line in enumerate(lines, 1):
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue

            # Rule 1: Check base image tagging
            if clean_line.startswith("FROM"):
                if ":latest" in clean_line or ":" not in clean_line.split()[1]:
                    findings += 1
                    print(f"{line_num:<6} | {'WARN':<8} | Base image uses 'latest' or unpinned tag. Specify a explicit version hash or version.")

            # Rule 2: Check for root user execution
            if clean_line.startswith("USER"):
                has_user_instruction = True
                if "root" in clean_line.lower():
                    findings += 1
                    print(f"{line_num:<6} | {'HIGH':<8} | Container explicitly set to run as privileged 'root' user.")

            # Rule 3: Check for HEALTHCHECK presence
            if clean_line.startswith("HEALTHCHECK"):
                has_healthcheck = True

            # Rule 4: Check sudo installation
            if "apt-get install" in clean_line and "sudo" in clean_line:
                findings += 1
                print(f"{line_num:<6} | {'HIGH':<8} | Installing 'sudo' in container images increases the attack surface.")

        if not has_user_instruction:
            findings += 1
            print(f"{'FILE':<6} | {'HIGH':<8} | Missing USER instruction. Container will run as root by default.")

        if not has_healthcheck:
            findings += 1
            print(f"{'FILE':<6} | {'INFO':<8} | Missing HEALTHCHECK instruction for container lifecycle tracking.")

        print(f"\n[*] Dockerfile Audit Complete. {findings} policy violation(s) flagged.")

    except FileNotFoundError:
        print(f"[-] Error: File '{dockerfile_path}' not found.")
    except Exception as e:
        print(f"[-] Dockerfile linting failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Dockerfile instructions for non-root enforcement and best practices")
    parser.add_argument("-d", "--dockerfile", required=True, type=Path, help="Path to Dockerfile")

    args = parser.parse_args()
    lint_dockerfile(args.dockerfile)