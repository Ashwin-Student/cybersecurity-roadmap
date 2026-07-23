import ast
import argparse
from pathlib import Path

class SecurityVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.issues = 0

    def visit_Call(self, node):
        # Check for dangerous function calls: eval() or exec()
        if isinstance(node.func, ast.Name):
            if node.func.id in ("eval", "exec"):
                print(f"  [!] HIGH RISK: Use of '{node.func.id}()' at line {node.lineno} in {self.filename}")
                self.issues += 1

        # Check for subprocess calls with shell=True
        if isinstance(node.func, ast.Attribute) and node.func.attr in ("Popen", "run", "call"):
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    print(f"  [!] CRITICAL: Subprocess with 'shell=True' at line {node.lineno} in {self.filename}")
                    self.issues += 1

        self.generic_visit(node)

def lint_python_file(file_path: Path) -> int:
    """Parse source file into AST and run security visitor."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=str(file_path))
        visitor = SecurityVisitor(file_path.name)
        visitor.visit(tree)
        return visitor.issues
    except SyntaxError as e:
        print(f"[-] Syntax error parsing {file_path}: {e}")
        return 0

def scan_codebase(target_dir: Path) -> None:
    """Recursively scan codebase for security issues."""
    print(f"[+] Running SAST audit on directory: {target_dir}\n")
    total_issues = 0
    scanned_files = 0

    for py_file in target_dir.rglob("*.py"):
        scanned_files += 1
        total_issues += lint_python_file(py_file)

    print(f"\n--- Static Analysis Complete ---")
    print(f"Files Inspected: {scanned_files}")
    print(f"Vulnerabilities Flagged: {total_issues}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Static Application Security Testing (SAST) linter for Python code")
    parser.add_argument("-d", "--dir", default=Path("."), type=Path, help="Target codebase directory")

    args = parser.parse_args()
    scan_codebase(args.dir)