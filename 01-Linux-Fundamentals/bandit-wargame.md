# OverTheWire: Bandit Wargame Write-ups & Core Linux Navigation

This document tracks my tactical solutions, command deep-dives, and the system security lessons learned while completing the Bandit Linux challenges.

---

## 🛠️ Core Commands Mastered Today
Before diving into the levels, these 6 fundamental commands are essential for navigating, hunting for, and analyzing data inside a Linux file system:

1. **`ls` (List):** Used to view what files and folders exist in the current directory. (e.g., `ls -a` to reveal hidden files).
2. **`cd` (Change Directory):** Used to move between different folders (e.g., `cd inhere` to move forward, `cd ..` to move backward).
3. **`cat` (Concatenate):** Used to quickly open a text file and read its contents directly inside the terminal screen.
4. **`file`:** Inspects a file's internal properties to determine its exact type (e.g., confirming if a file is plain text, an executable program, or a compressed ZIP archive, bypassing fake extensions).
5. **`du` (Disk Usage):** Measures how much storage space files or folders are consuming on the hard drive (crucial for finding massive data dumps or hidden archives).
6. **`find`:** Searches the entire computer for specific files based on parameters like name, size, user ownership, or file permissions.

---

## 🎯 Level 0 ➔ Level 1
* **Objective:** Establish a secure remote baseline connection to the target server via SSH.
* **Core Commands:** `ssh bandit0@bandit.labs.overthewire.org -p 2220`
* **Key Lesson:** The `-p` parameter is mandatory to declare a non-standard network port (2220 instead of the default 22), bypassing strict local network infrastructure or campus firewall blockages.

## 🎯 Level 1 ➔ Level 2
* **Objective:** Read the hidden token string located inside a file named `-`.
* **Core Commands:** `ls`, `cat ./-`
* **Key Lesson:** In Linux environments, a single dash `-` is inherently parsed as an option flag introduction rather than a string identifier. Prefixes like `./` force the engine to process the input cleanly as a relative directory path pointer.

## 🎯 Level 2 ➔ Level 3
* **Objective:** Extract data from a multi-word file named `--spaces in this filename--`.
* **Core Commands:** `ls`, `cat "./--spaces in this filename--"`
* **Key Lesson:** Spaces act as input segment dynamic dividers in the terminal. Enclosing parameter targets within strict double quotes `""` ensures the entire sequence is evaluated as a unified object argument. Adding `./` prevents the leading double dashes from breaking the `cat` command.

## 🎯 Level 3 ➔ Level 4
* **Objective:** Locate and read a hidden file inside the `inhere` folder.
* **Core Commands:** `cd inhere`, `ls`, `ls -a`, `cat .hidden`
* **Key Lesson:** Any file or folder starting with a literal dot (`.` ) is completely hidden from the standard `ls` command view. Using the **`ls -a`** (List All) flag exposes these hidden items.
