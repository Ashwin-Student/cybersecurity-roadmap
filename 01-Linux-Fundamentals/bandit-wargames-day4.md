# OverTheWire: Bandit Wargame Write-ups & Network Triage

This document tracks my tactical solutions, command pipelines, and core security lessons learned during today's session.

---

## 🛠️ Linux Command Blueprint (Today's Network Utilities)
These are the core network diagnostics and connectivity tools leveraged today to transmit secrets across local ports and establish secure streams.

### 1. Secure Authentication & Remote Access
* **`ssh -i [private_key]`**: Establishes a Secure Shell connection using an asymmetric private key file for passwordless authentication instead of entering a plaintext string.

### 2. Network Utilities & Socket Connections
* **`nc` (Netcat):** Known as the "Swiss Army knife" of networking. Used to open raw TCP/UDP connections to listen on or send data directly to specific port numbers.
* **`openssl s_client`:** A diagnostic tool used to establish secure, encrypted SSL/TLS connections to remote servers or local services, bypassing raw text inspection.

---

## 🎯 Level 13 ➔ Level 14
* **Objective:** Authenticate as the next user using a private SSH key stored on the server.
* **Core Commands:** `ssh -i sshkey.private bandit14@localhost -p 2220`
* **Key Lesson:** Storing private keys with weak permissions or keeping them accessible on a shared server presents a massive privilege escalation risk. The `-i` flag forces SSH to use a private key file for instant identity verification.

## 🎯 Level 14 ➔ Level 15
* **Objective:** Submit the current level's password to a local network port to receive the next credential.
* **Core Commands:** `nc localhost 30000`
* **Key Lesson:** Netcat allows you to interact directly with internal network services running locally on a system (`localhost`). Interrogating ports via `nc` helps maps out active local daemons.

## 🎯 Level 15 ➔ Level 16
* **Objective:** Transmit a password securely to an internal port requiring SSL/TLS encryption.
* **Core Commands:** `openssl s_client -connect localhost:30001`
* **Key Lesson:** Modern infrastructure blocks or ignores unencrypted traffic. When standard Netcat fails against an encrypted service, `openssl s_client` handles the TLS handshake automatically, providing a raw, secure communication channel to the service.
