import struct
import argparse
from pathlib import Path

# IMAGE_DLLCHARACTERISTICS flags
IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE = 0x0040  # ASLR
IMAGE_DLLCHARACTERISTICS_NX_COMPAT   = 0x0100  # DEP / NX

def lint_pe_header(pe_path: Path) -> None:
    """Inspect PE header bytes for ASLR and DEP memory protection flags."""
    print(f"[+] Inspecting PE binary header: {pe_path}\n")

    try:
        with open(pe_path, "rb") as f:
            # Verify DOS Header signature ("MZ")
            dos_header = f.read(64)
            if len(dos_header) < 64 or dos_header[:2] != b"MZ":
                print("[-] Error: File is not a valid PE binary (missing 'MZ' header).")
                return

            # Extract e_lfanew offset to PE header
            e_lfanew = struct.unpack_from("<I", dos_header, 0x3C)[0]
            f.seek(e_lfanew)

            # Verify PE Header signature ("PE\0\0")
            pe_signature = f.read(4)
            if pe_signature != b"PE\x00\x00":
                print("[-] Error: Invalid PE signature.")
                return

            # Read File Header (20 bytes) to get size of Optional Header
            file_header = f.read(20)
            size_of_optional_header = struct.unpack_from("<H", file_header, 16)[0]

            if size_of_optional_header == 0:
                print("[-] Error: Optional header missing.")
                return

            # Read Optional Header
            optional_header = f.read(size_of_optional_header)
            magic = struct.unpack_from("<H", optional_header, 0)[0]

            # Determine offset of DllCharacteristics based on PE32 (0x10B) or PE32+ (0x20B)
            if magic == 0x10B:
                dll_char_offset = 70
            elif magic == 0x20B:
                dll_char_offset = 70
            else:
                print("[-] Error: Unknown PE magic number.")
                return

            dll_characteristics = struct.unpack_from("<H", optional_header, dll_char_offset)[0]

            has_aslr = bool(dll_characteristics & IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE)
            has_dep = bool(dll_characteristics & IMAGE_DLLCHARACTERISTICS_NX_COMPAT)

            print("--- Compiler Security Mitigation Status ---")
            print(f"  ASLR (Dynamic Base): {'ENABLED' if has_aslr else 'DISABLED [!]'}")
            print(f"  DEP / NX (No-Execute): {'ENABLED' if has_dep else 'DISABLED [!]'}")

            if not has_aslr or not has_dep:
                print("\n[!] WARNING: Binary lacks standard memory corruption mitigations.")
            else:
                print("\n[PASS] Binary includes both ASLR and DEP mitigation flags.")

    except FileNotFoundError:
        print(f"[-] Error: File '{pe_path}' not found.")
    except Exception as e:
        print(f"[-] PE header parsing failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lint Windows PE binary headers for ASLR and DEP flags")
    parser.add_argument("-b", "--binary", required=True, type=Path, help="Path to Windows EXE or DLL file")

    args = parser.parse_args()
    lint_pe_header(args.binary)