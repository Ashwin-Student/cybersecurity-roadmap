import secrets
import string
import argparse

def generate_hex_token(nbytes: int = 32) -> str:
    """Generate a secure hex-encoded API token or secret key."""
    return secrets.token_hex(nbytes)

def generate_url_safe_token(nbytes: int = 32) -> str:
    """Generate a Base64-URL-safe token ideal for session keys."""
    return secrets.token_urlsafe(nbytes)

def generate_complex_passphrase(length: int = 24) -> str:
    """Generate a high-entropy password containing letters, digits, and special characters."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return "".join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cryptographically Secure Key Generator")
    parser.add_argument("-t", "--type", choices=["hex", "url", "pass"], default="hex", help="Token format")
    parser.add_argument("-l", "--length", type=int, default=32, help="Length / byte size")

    args = parser.parse_args()

    print("\n--- Secure Entropy Generator ---")
    if args.type == "hex":
        val = generate_hex_token(args.length)
        print(f"Hex Token ({len(val)} chars): {val}")
    elif args.type == "url":
        val = generate_url_safe_token(args.length)
        print(f"URL-Safe Token ({len(val)} chars): {val}")
    else:
        val = generate_complex_passphrase(args.length)
        print(f"Complex Passphrase ({args.length} chars): {val}")