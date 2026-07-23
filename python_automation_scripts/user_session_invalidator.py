import json
import argparse
from datetime import datetime
from pathlib import Path

def build_session_revocation_payload(username: str, output_file: Path) -> None:
    """Generate identity provider API payload to terminate active user tokens."""
    print(f"[+] Initiating Session Revocation Playbook for Target User: {username}")

    revocation_payload = {
        "action": "REVOKE_ALL_SESSIONS",
        "target_user": username,
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "operations": [
            {"type": "INVALIDATE_REFRESH_TOKENS", "status": "PENDING"},
            {"type": "CLEAR_ACTIVE_SESSIONS", "status": "PENDING"},
            {"type": "FORCE_PASSWORD_RESET_ON_NEXT_LOGIN", "status": "REQUIRED"}
        ],
        "metadata": {
            "triggered_by": "SOC_Automated_Playbook",
            "reason": "Compromised Credentials / Account Takeover Detection"
        }
    }

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(revocation_payload, f, indent=4)

        print(f"[+] Identity containment payload created successfully: {output_file}")
        print("  [*] Ready to post to IdP endpoint (e.g., Azure AD / Okta / Keycloak).")

    except Exception as e:
        print(f"[-] Failed to build payload: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build session revocation payload for compromised accounts")
    parser.add_argument("-u", "--user", required=True, help="Target username or User Principal Name (UPN)")
    parser.add_argument("-o", "--output", default=Path("session_revoke_request.json"), type=Path, help="Output payload path")

    args = parser.parse_args()
    build_session_revocation_payload(args.user, args.output)