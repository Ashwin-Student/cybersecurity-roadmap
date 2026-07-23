import re
import argparse
from pathlib import Path

LINT_RULES = [
    {
        "id": "DOCKER-SEC-01",
        "name": "Root User Execution",
        "pattern": re.compile(r"^\s*USER\s+(?!root\b)[a-zA-Z0-9_-]+", re.IGNORECASE),
        "invert": True,  # Flag if valid USER is MISSING
        "severity": "HIGH",
        "description": "Container runs as default root user. Specify a non-root USER."
    },
    {
        "id": "DOCKER-SEC-02",
        "name": "Unpinned Base Image Tag ('latest')",
        "pattern": re.compile(r"^\s*FROM\s+[\w./-]+:latest", re.IGNORECASE),
        "severity": "MEDIUM",
        "description": "Avoid using ':latest' tag for base images to ensure build reproducibility."
    },
    {
        "id": "DOCKER-SEC-03",
        "name": "Potential Secret in ENV Directive",
        "pattern": re.compile(r"^\s*ENV\s+.*(?:password|secret|key|token)\s*=", re.IGNORECASE),
        "severity": "CRITICAL",
        "description": "Do not hardcode secrets in ENV instructions; use build secrets or runtime mounts."
    }
]

def lint_dockerfile(dockerfile_path: Path) -> None:
    """Analyze a Dockerfile for security risks and compliance issues."""
    print(f"[+] Auditing Dockerfile: {dockerfile_path}\n")

    if not dockerfile_path.exists():
        print(f"[-] File '{dockerfile_path}' not found.")
        return

    try:
        with open(dockerfile_path, "r", encoding="utf-8") as f:
            content = f.read()

        violations = 0

        for rule in LINT_RULES:
            match = rule["pattern"].search(content)
            should_flag = not match if rule.get("invert") else match

            if should_flag:
                violations += 1
                print(f"  [{rule['severity']}] {rule['id']}: {rule['name']}")
                print(f"         {rule['description']}\n")

        print(f"[*] Audit Complete. Total Policy Violations Found: {violations}")

    except Exception as e:
        print(f"[-] Failed to lint Dockerfile: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lint Dockerfile templates for container security best practices")
    parser.add_argument("-f", "--file", required=True, type=Path, help="Path to Dockerfile manifest")

    args = parser.parse_args()
    lint_dockerfile(args.file)