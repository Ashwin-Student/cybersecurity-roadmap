import base64
import json
import argparse
from datetime import datetime, timezone

def decode_base64_url(segment: str) -> dict:
    """Decode Base64URL-encoded JWT segment to a dictionary."""
    # Add padding if required
    rem = len(segment) % 4
    if rem > 0:
        segment += "=" * (4 - rem)
    
    decoded_bytes = base64.urlsafe_b64decode(segment)
    return json.loads(decoded_bytes.decode("utf-8"))

def audit_jwt(jwt_token: str) -> None:
    """Parse JWT claims and highlight security misconfigurations."""
    parts = jwt_token.strip().split(".")
    if len(parts) != 3:
        print("[-] Invalid JWT structure! Expected 3 dot-separated segments (Header.Payload.Signature).")
        return

    try:
        header = decode_base64_url(parts[0])
        payload = decode_base64_url(parts[1])

        print("\n--- JWT Header Analysis ---")
        print(json.dumps(header, indent=2))
        
        algorithm = header.get("alg", "UNKNOWN").upper()
        if algorithm == "NONE":
            print("  [!] CRITICAL: Token uses 'alg: none'! Signature verification is bypassed.")
        elif algorithm.startswith("HS"):
            print("  [*] Note: Symmetric HMAC algorithm detected. Ensure secret key entropy is high.")

        print("\n--- JWT Payload Claims ---")
        print(json.dumps(payload, indent=2))

        # Expiration Check
        exp = payload.get("exp")
        if exp:
            exp_date = datetime.fromtimestamp(exp, tz=timezone.utc)
            now = datetime.now(timezone.utc)
            print(f"\n[*] Token Expiration (exp): {exp_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            if now > exp_date:
                print("  [!] ALERT: Token has EXPIRED!")
            else:
                print("  [+] Token is currently within valid timeframe.")
        else:
            print("\n  [!] WARNING: Missing 'exp' (Expiration Time) claim in token payload!")

    except Exception as e:
        print(f"[-] Failed to parse JWT segments: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decode and Audit JSON Web Token (JWT) claims")
    parser.add_argument("-t", "--token", required=True, help="Raw JWT string (Header.Payload.Signature)")
    
    args = parser.parse_args()
    audit_jwt(args.token)