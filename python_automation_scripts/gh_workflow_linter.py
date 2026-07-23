import argparse
import re
from pathlib import Path

# Patterns indicating unpinned or dynamic action versions
DYNAMIC_VERSION_PATTERN = re.compile(r'uses:\s*[\'"]?([^\s@]+)@(main|master|v\d+[\.\d+]*)[\'"]?', re.IGNORECASE)

def lint_github_workflow(workflow_path: Path) -> None:
    """Inspect a GitHub Actions workflow file for security risky patterns."""
    print(f"[+] Linting GitHub Actions workflow: {workflow_path}\n")

    try:
        with open(workflow_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        findings = 0
        has_permissions_block = False

        print(f"{'Line':<6} | {'Severity':<8} | {'Issue Description'}")
        print("-" * 75)

        for line_num, line in enumerate(lines, 1):
            line_str = line.strip()

            if "permissions:" in line_str:
                has_permissions_block = True

            # Check 1: Unpinned third-party actions
            match = DYNAMIC_VERSION_PATTERN.search(line_str)
            if match:
                action_name, ref = match.group(1), match.group(2)
                findings += 1
                print(f"{line_num:<6} | {'WARN':<8} | Action '{action_name}' is pinned to branch/tag '{ref}' instead of a full commit SHA.")

            # Check 2: Inline pull_request_target checkout risk
            if "pull_request_target" in line_str:
                findings += 1
                print(f"{line_num:<6} | {'HIGH':<8} | 'pull_request_target' trigger detected. Ensure untrusted PR code is not executed.")

        if not has_permissions_block:
            findings += 1
            print(f"{'FILE':<6} | {'WARN':<8} | No top-level 'permissions:' block defined. Default token permissions may be overly broad.")

        print(f"\n[*] Workflow Audit Complete. {findings} issue(s) identified.")

    except FileNotFoundError:
        print(f"[-] Error: File '{workflow_path}' not found.")
    except Exception as e:
        print(f"[-] Workflow linting failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lint GitHub Actions workflows for supply chain and permission risks")
    parser.add_argument("-w", "--workflow", required=True, type=Path, help="Path to GitHub workflow YAML file")

    args = parser.parse_args()
    lint_github_workflow(args.workflow)