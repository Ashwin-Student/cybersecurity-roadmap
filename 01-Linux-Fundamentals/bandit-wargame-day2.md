# OverTheWire: Bandit Wargame Write-ups & Core Linux Navigation

This document tracks my tactical solutions, command deep-dives, and the system security lessons learned during today's session.

---

## 🛠️ Linux Command Blueprint (Today's Utilities)
These are the core tools leveraged today to analyze file signatures, hunt across the root system, and filter massive data logs.

### 1. File Identification & Evaluation
* **`file` (File Type Triage):** Analyzes the structural header signature of a target object to determine its true format, ignoring fake extensions.
  * `file ./*`: Wildcard scanning used today to quickly distinguish unreadable binary `data` from human-readable `ASCII text`.

### 2. Advanced Hunting & Error Handling
* **`find` (System-Wide Search):** Scans the file system hierarchy for objects matching explicit administrative parameters.
  * `-type f`: Restricts search parameters strictly to files, filtering out folders.
  * `-size [X]c`: Targets files matching an exact byte size (where `c` explicitly denotes bytes).
  * `! -executable`: Acts as a boolean `NOT` operator to exclude executable binaries or scripts.
  * `2>/dev/null`: Redirects Standard Error (stderr) outputs into a system void, muting "Permission Denied" alerts when scanning the system root (`/`).

### 3. Data Processing & Text Filtering
* **`grep` (Global Regular Expression Print):** Acts as a high-speed text search engine, filtering massive data dumps to print only the specific lines containing a designated keyword string.
* **`|` (The Pipe):** A powerful command redirector that takes the data output (`stdout`) of a preceding command and feeds it straight as input (`stdin`) into the next program.

---

## 🎯 Level 4 ➔ Level 5
* **Objective:** Identify the single human-readable file out of 10 mixed data files.
* **Core Commands:** `file ./*`, `cat ./-file07`
* **Key Lesson:** The `file` command looks past extensions to read a file's header signature. This allows a security analyst to instantly identify raw `data` dumps versus readable `ASCII text` before opening a potentially corrupt or malicious file.

## 🎯 Level 5 ➔ Level 6
* **Objective:** Hunt down a file hidden deep within 20 nested directories based on exact properties.
* **Core Commands:** `find . -type f -size 1033c ! -executable`
* **Key Lesson:** The `find` utility handles heavy system scanning. By specifying specific parameters—such as `-type f` (files only), `-size 1033c` (exactly 1033 bytes), and `! -executable` (not a script)—you can filter out thousands of dummy files instantly.

## 🎯 Level 6 ➔ Level 7
* **Objective:** Scan the entire operating system root for a specific file owned by a distinct user and group.
* **Core Commands:** `find / -user bandit7 -group bandit6 -size 33c 2>/dev/null`
* **Key Lesson:** Searching the entire OS system root (`/`) triggers hundreds of "Permission Denied" alerts. Appending **`2>/dev/null`** actively redirects standard error outputs (stderr) into a system void, leaving only the clean, successful file path on screen.

## 🎯 Level 7 ➔ Level 8
* **Objective:** Extract a needle-in-a-haystack credential string hidden inside a massive data file.
* **Core Commands:** `cat data.txt | grep millionth`
* **Key Lesson:** The Pipe (`|`) takes the stdout of one program and feeds it as stdin to another. Combining `cat` with **`grep`** creates a quick command-line search engine, pulling only the string data containing the key match word.
