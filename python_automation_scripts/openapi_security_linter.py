import json
import argparse
from pathlib import Path

def audit_openapi_security(schema_path: Path) -> None:
    """Inspect OpenAPI specification to ensure all endpoints enforce authentication."""
    print(f"[+] Loading OpenAPI Schema: {schema_path}\n")

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        global_security = schema.get("security", [])
        paths = schema.get("paths", {})

        print(f"--- Schema Overview ---")
        print(f"Title: {schema.get('info', {}).get('title', 'Untitled API')}")
        print(f"Global Security Directives Configured: {len(global_security) > 0}\n")

        unprotected_endpoints = 0

        for path_name, methods in paths.items():
            if not isinstance(methods, dict):
                continue

            for http_method, details in methods.items():
                if http_method.lower() in ("get", "post", "put", "delete", "patch"):
                    # Endpoint-level security overrides global security
                    has_endpoint_sec = "security" in details
                    effective_sec = details.get("security", global_security)

                    if not effective_sec or len(effective_sec) == 0:
                        unprotected_endpoints += 1
                        print(f"  [!] UNPROTECTED ENDPOINT: {http_method.upper():<6} {path_name}")

        print(f"\n[*] Audit Complete.")
        if unprotected_endpoints == 0:
            print("  [PASS] All endpoints declare active authentication directives.")
        else:
            print(f"  [WARN] Found {unprotected_endpoints} endpoint(s) lacking authentication declarations.")

    except FileNotFoundError:
        print(f"[-] Error: File '{schema_path}' not found.")
    except Exception as e:
        print(f"[-] Failed to parse OpenAPI JSON schema: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit OpenAPI/Swagger JSON specifications for missing endpoint security")
    parser.add_argument("-s", "--schema", required=True, type=Path, help="Path to OpenAPI JSON schema file")

    args = parser.parse_args()
    audit_openapi_security(args.schema)