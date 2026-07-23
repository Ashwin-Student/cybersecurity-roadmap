import re
import argparse
from pathlib import Path

# Matches standard DB URIs: protocol://user:password@host:port/dbname
DB_URI_REGEX = re.compile(
    r'(?P<proto>postgres(?:ql)?|mysql|mariadb|mssql|oracle|mongodb(?:\+srv)?)://'
    r'(?P<user>[^:\s]+):(?P<password>[^@\s]+)@'
    r'(?P<host>[^/\s:]+)(?::(?P<port>\d+))?/(?P<db>[^\s\?]+)',
    re.IGNORECASE
)

def sanitize_connection_strings(config_path: Path) -> None:
    """Find and mask credentials inside SQL connection strings."""
    print(f"[+] Scanning file for embedded DB credentials: {config_path}\n")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()

        matches = list(DB_URI_REGEX.finditer(content))

        if not matches:
            print("[PASS] No hardcoded database connection strings identified.")
            return

        print(f"[!] Found {len(matches)} exposed database URI(s):\n")

        for m in matches:
            proto = m.group("proto")
            user = m.group("user")
            raw_uri = m.group(0)
            
            # Mask password
            sanitized_uri = DB_URI_REGEX.sub(
                r'\g<proto>://\g<user>:********@\g<host>:\g<port>/\g<db>',
                raw_uri
            )
            
            print(f"  Exposed User:     {user} ({proto})")
            print(f"  Sanitized URI:    {sanitized_uri}\n")

    except FileNotFoundError:
        print(f"[-] Error: File '{config_path}' not found.")
    except Exception as e:
        print(f"[-] Connection string audit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect and redact hardcoded DB passwords in connection URIs")
    parser.add_argument("-c", "--config", required=True, type=Path, help="Path to config file or env dump")

    args = parser.parse_args()
    sanitize_connection_strings(args.config)