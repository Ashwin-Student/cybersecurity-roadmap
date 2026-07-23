import base64
import urllib.parse
import re
import argparse

def is_hex(s: str) -> bool:
    """Check if string is valid hex-encoded data."""
    s = s.strip()
    return bool(re.fullmatch(r"(?:[0-9a-fA-F]{2})+", s))

def is_base64(s: str) -> bool:
    """Check if string matches standard Base64 encoding structure."""
    s = s.strip()
    if len(s) % 4 != 0:
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s))

def auto_decode(payload: str, max_depth: int = 5) -> None:
    """Recursively attempt decoding multi-layered obfuscated strings."""
    current = payload.strip()
    depth = 0

    print(f"\n--- Multi-Layer Decoder Trace ---")
    print(f"Input: {current}\n")

    while depth < max_depth:
        decoded = None
        method = ""

        # Check URL Encoding
        if "%" in current:
            unquoted = urllib.parse.unquote(current)
            if unquoted != current:
                decoded = unquoted
                method = "URL Encoding"

        # Check Hex Encoding
        elif is_hex(current):
            try:
                decoded = bytes.fromhex(current).decode("utf-8", errors="ignore")
                method = "Hexadecimal"
            except Exception:
                pass

        # Check Base64 Encoding
        elif is_base64(current):
            try:
                raw_bytes = base64.b64decode(current)
                decoded = raw_bytes.decode("utf-8", errors="ignore")
                method = "Base64"
            except Exception:
                pass

        if decoded and decoded != current:
            depth += 1
            print(f"[Layer {depth}] Decoded via {method}:")
            print(f"          {decoded}")
            current = decoded
        else:
            if depth == 0:
                print("[-] No common encodings (Base64, Hex, URL) identified.")
            else:
                print(f"\n[+] Final Fully Decoded Output:\n{current}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursively detect and decode encoded payload strings")
    parser.add_argument("-p", "--payload", required=True, help="Encoded payload string")
    
    args = parser.parse_args()
    auto_decode(args.payload)