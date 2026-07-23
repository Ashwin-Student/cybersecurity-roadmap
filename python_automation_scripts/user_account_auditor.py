import os
import pwd
import argparse

def audit_local_users() -> None:
    """Inspect system user accounts for elevated privileges and login shells."""
    print("\n--- System User Account Audit ---")
    
    try:
        users = pwd.getpwall()
    except Exception as e:
        print(f"[-] Error retrieving user database: {e}")
        return

    uid_zero_users = []
    login_users = []
    
    # Standard non-login shells
    NOLOGIN_SHELLS = {"/usr/sbin/nologin", "/bin/false", "/dev/null", "/sbin/nologin"}

    for user in users:
        username = user.pw_name
        uid = user.pw_uid
        shell = user.pw_shell

        # Check for non-root users with UID 0 (Root privileges)
        if uid == 0 and username != "root":
            uid_zero_users.append(username)

        # Check for interactive login accounts
        if shell not in NOLOGIN_SHELLS:
            login_users.append((username, uid, shell))

    # Output UID 0 Alerts
    if uid_zero_users:
        print("[!] CRITICAL: Non-root accounts found with UID 0 (Root privileges):")
        for u in uid_zero_users:
            print(f"    - Username: {u}")
    else:
        print("[+] STATUS: No unauthorized UID 0 accounts detected.")

    # Output Interactive Users
    print(f"\n[*] Found {len(login_users)} account(s) with interactive login shells:")
    for username, uid, shell in login_users:
        category = "System User" if uid < 1000 else "Standard/Human User"
        print(f"    - {username:<15} (UID: {uid:<5}) | Shell: {shell:<15} | Type: {category}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit local system users and privileges")
    args = parser.parse_args()

    if os.name != "posix":
        print("[-] This script uses the 'pwd' module designed for POSIX/Linux systems.")
    else:
        audit_local_users()