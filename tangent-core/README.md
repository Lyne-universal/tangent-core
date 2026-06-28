# Tangent Core

Lyne Universal Systems // Tangent Core — local-first system data inspector & security scrub engine.

## Features
- Line-by-line redaction of sensitive data in text/env/log files
- Assignment-aware redaction (e.g., `SECRET_KEY=...` becomes `SECRET_KEY=[REDACTED]`)
- Detects exposed token-like strings (basic heuristic)
- Detects sensitive paths (e.g., `/home`, `/Users`, `C:\\Users\\...`)
- Writes a scrubbed output file (`<input>.scrubbed`)
- Emits a JSON report to stdout
- Includes a lightweight GUI dashboard (`tangent_gui.py`)

## Installation
```bash
cd tangent-core
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage (CLI)
### Version
```bash
python tangent_core.py version
```

### Scan a file
```bash
python tangent_core.py scan sample.env
```

Creates:
- `sample.env.scrubbed`
- prints a JSON report to stdout

## CLI examples
```bash
python tangent_core.py scan /path/to/.env
python tangent_core.py scan /path/to/app.log
```

## GUI
Run:
```bash
python tangent_gui.py
```
Then:
1. Select a target file
2. View the sanitized preview
3. Export the safe copy

## Example output
Input (`sample.env`):
- `SECRET_KEY=my-super-secret-key-123456`
- `HOME=/home/raymond`

Output:
- `SECRET_KEY=[REDACTED]`
- `HOME=[REDACTED]`

## Project structure
- `tangent_core.py` — core engine + CLI
- `tangent_gui.py` — GUI wrapper
- `tests/` — unit tests
- `sample.env` — example secrets for demonstration

