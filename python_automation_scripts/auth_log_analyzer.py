import re
import argparse
from collections import defaultdict

# Regex matching standard Linux SSH auth log entries for failed attempts
FAILED_PASSWORD_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
)

def parse_auth_log(log_path: str, threshold: int = 5) -> None:
    """Read an authentication log file and flag suspicious failed login counts."""
    failed_attempts = defaultdict(int)
    targeted_users = defaultdict(set)

    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = FAILED_PASSWORD_PATTERN.search(line)
                if match:
                    ip = match.group("ip")
                    user = match.group("user")
                    failed_attempts[ip] += 1
                    targeted_users[ip].add(user)

        print(f"\n--- SSH Authentication Failure Summary ({log_path}) ---")
        suspicious_found = False

        for ip, count in failed_attempts.items():
            if count >= threshold:
                suspicious_found = True
                users_list = ", ".join(list(targeted_users[ip])[:5]) # Show up to 5 usernames
                print(f"[!] SUSPICIOUS IP: {ip} | Failed Attempts: {count} | Targeted Users: {users_list}")

        if not suspicious_found:
            print(f"[*] No IP addresses exceeded the threshold of {threshold} failed attempts.")

    except FileNotFoundError:
        print(f"[-] Error: File not found at {log_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Linux auth log for SSH brute-force activity.")
    parser.add_argument("-f", "--file", default="/var/log/auth.log", help="Path to auth.log file")
    parser.add_argument("-t", "--threshold", type=int, default=5, help="Alert threshold for failed attempts")
    
    args = parser.parse_args()
    parse_auth_log(args.file, args.threshold)