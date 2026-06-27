The core local-first system data inspection and security scrubbing engine for the **Lyne Aegis** division.

## Overview
This core utility handles automated, client-side token parsing and pattern extraction entirely within localized runtime environments. It actively scans input streams, flags potential vulnerability leaks (such as exposed credentials or system directories), and instantly processes them into clean, structured, auditable JSON logs without relying on external cloud processing.

## Quickstart
Run the core script natively using standard Python flags:
```bash
python aegis_core.py