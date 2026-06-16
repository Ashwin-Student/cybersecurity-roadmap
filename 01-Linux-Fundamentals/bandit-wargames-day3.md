# OverTheWire: Bandit Wargame Write-ups & System Triage

This document tracks my tactical solutions, command pipelines, and core security lessons learned during today's session.

---

## 🛠️ Linux Command Blueprint (Today's Utilities)
These are the core text-filtering, cryptographic, and archive tools leveraged today to isolate unique signatures, decode data, and extract hidden assets.

### 1. Data Sorting & Deduplication
* **`sort`:** Rearranges file lines alphabetically. This is required before running matching utilities because duplicate lines must sit directly next to each other to be parsed.
* **`uniq -u`:** Filters a text stream and prints **only** the lines that are completely unique, stripping away any data that repeats even once.

### 2. Cryptography & Reverse Engineering
* **`strings`:** Scans binary files and filters out corrupted system blocks, displaying only human-readable text sequences.
* **`base64 -d`:** Decodes data blocks that have been obscured using Base64 encoding schemas back into raw text.
* **`tr '[Set1]' '[Set2]'` (Translate):** Maps and swaps a string of input characters to an output set. Used to cleanly decode **ROT13** text by rotating letters 13 spaces.
* **`xxd -r`:** Reverses a plain text hex dump back into its original raw binary file format.

### 3. Archive & Compression Management
* **`gunzip`:** Decompresses `.gz` archive files (Gzip format).
* **`bunzip2`:** Decompresses `.bz2` archive files (Bzip2 format).
* **`tar -xf`:** Extracts files from tape archive (`.tar`) containers.

---

## 🎯 Level 8 ➔ Level 9
* **Objective:** Identify a completely unique line of text within a massive log file filled with repeating data clutter.
* **Core Commands:** `sort data.txt | uniq -u`
* **Key Lesson:** Pairing `sort` with `uniq -u` via a pipeline filters out system noise. It strips away all recurring events, cleanly printing the one anomalous event (the password).

## 🎯 Level 9 ➔ Level 10
* **Objective:** Recover plain text credentials hidden inside a corrupted binary data file.
* **Core Commands:** `strings data.txt | grep "=="`
* **Key Lesson:** Using standard commands on raw binary data corrupts terminal sessions. The `strings` utility isolates embedded readable ASCII data, allowing regular tools like `grep` to parse it safely.

## 🎯 Level 10 ➔ Level 11
* **Objective:** Decode a password string that has been obscured using Base64 encoding.
* **Core Commands:** `base64 -d data.txt`
* **Key Lesson:** Base64 is used to convert binary data into safe ASCII text for transport. Appending the `-d` (decode) flag reverses this transmission mapping to instantly print the raw plaintext.

## 🎯 Level 11 ➔ Level 12
* **Objective:** Decrypt a text file obfuscated using a Caesar cipher substitution pattern (ROT13).
* **Core Commands:** `cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'`
* **Key Lesson:** The `tr` (translate) command easily handles character mapping. Shifting a letter 13 spaces twice in a 26-letter alphabet effectively breaks basic string-obfuscation layers used by legacy systems or malware payloads.

## 🎯 Level 12 ➔ Level 13
* **Objective:** Perform a digital forensics analysis to decompress a heavily recursive, multi-layered file archive.
* **Core Commands:** `mkdir /tmp/ashwin_labs`, `xxd -r`, `gunzip`, `bunzip2`, `tar -xf`
* **Key Lesson:** Malware scripts and system packages often use nested compression to hide assets. Reversing the hex data with `xxd` and continuously triaging with `file` enables an analyst to peel back custom multi-format archives step-by-step.
