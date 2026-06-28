# Tangent

Lyne Universal Systems // Tangent — local-first system data inspector & security scrub engine.

## Features
- Detects common secret patterns (basic heuristic)
- Detects sensitive paths (e.g., `/home`, `/Users`, `C:\\Users\\...`)
- Assignment-aware redaction: `KEY=VALUE` becomes `KEY=[REDACTED]`
- CLI scan that writes a scrubbed output file and prints a JSON report
- Desktop GUI dashboard for preview + export

## Installation
```bash
cd tangent-core
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
### CLI
```bash
cd tangent-core
python tangent_core.py version
python tangent_core.py scan sample.env
```

### GUI
```bash
cd tangent-core
python tangent_gui.py
```

## CLI examples
```bash
python tangent_core.py scan /path/to/app.log
python tangent_core.py scan /path/to/.env
```

## GUI
Select a target file, then export the scrubbed safe copy.

## Example output
Input:
- `SECRET_KEY=my-super-secret-key-123456`
- `HOME=/home/raymond`

Output:
- `SECRET_KEY=[REDACTED]`
- `HOME=[REDACTED]`

## Project structure
- `tangent-core/tangent_core.py` — core engine + CLI
- `tangent-core/tangent_gui.py` — GUI wrapper
- `tangent-core/tests/` — unit tests
- `tangent-core/sample.env` — sample secrets

