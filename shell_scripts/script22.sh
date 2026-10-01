#!/bin/bash
# ==============================================================================
# Script 22: Ping simulation for a list of servers
# ==============================================================================

echo "--- Script 22: Server Ping Simulator ---"

# Define an array with hardcoded server identifiers
SERVERS=("web1" "web2" "db1")

# Iterate through each element in the array
# "${SERVERS[@]}" expands to all elements in the array individually
for server in "${SERVERS[@]}"; do
    # Print simulated ping success message with realistic networking details
    echo "[+] Simulating ping to ${server}... Reply from 192.168.1.10: bytes=32 time=2ms TTL=64"
done

echo ""
