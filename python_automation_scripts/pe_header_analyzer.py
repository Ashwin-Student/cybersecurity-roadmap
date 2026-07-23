import struct
import argparse
from pathlib import Path

def parse_pe_header(pe_path: Path) -> None:
    """Parse basic DOS and PE headers of a Windows binary without external dependencies."""
    print(f"[+] Inspecting PE Header: {pe_path}\n")

    try:
        with open(pe_path, "rb") as f:
            # Check DOS Magic ('MZ')
            dos_header = f.read(64)
            if len(dos_header) < 64 or dos_header[:2] != b"MZ":
                print("[-] Invalid file: Missing 'MZ' DOS header.")
                return

            # Extract e_lfanew offset to PE header
            e_lfanew = struct.unpack("<I", dos_header[60:64])[0]
            f.seek(e_lfanew)

            # Check PE Signature ('PE\0\0')
            pe_sig = f.read(4)
            if pe_sig != b"PE\x00\x00":
                print("[-] Invalid PE Signature.")
                return

            # Read COFF File Header (20 bytes)
            coff_header = f.read(20)
            machine, num_sections, timestamp, _, _, opt_header_size, characteristics = struct.unpack("<HHIIIHH", coff_header)

            machine_type = "x64" if machine == 0x8664 else ("x86" if machine == 0x014c else f"Unknown ({hex(machine)})")

            print("--- PE COFF Header Summary ---")
            print(f"Target Architecture : {machine_type}")
            print(f"Number of Sections  : {num_sections}")
            print(f"Time Date Stamp     : {timestamp} (Unix Epoch)")
            print(f"Optional Header Size: {opt_header_size} bytes")
            print(f"Characteristics     : {hex(characteristics)}")

    except FileNotFoundError:
        print(f"[-] Error: File '{pe_path}' not found.")
    except Exception as e:
        print(f"[-] Failed to parse PE file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract COFF PE header metadata from executable files")
    parser.add_argument("-f", "--file", required=True, type=Path, help="Path to executable binary (.exe / .dll)")

    args = parser.parse_args()
    parse_pe_header(args.file)