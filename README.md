# tangent-core

The core local-first system data inspection and security scrubbing engine for the **Tangent** security division of **Lyne Universal Systems**.

## Overview
**Tangent** acts as a straight line intersecting your data streams at the edge—monitoring activity closely but ensuring external vulnerabilities never penetrate your local architecture. 

This core engine handles automated, client-side token parsing, cryptographic key tracking, and systemic pattern extraction entirely within localized runtime environments. It intercepts potential leak profiles (such as exposed credentials or system paths) and refactors them into structured, redacted JSON logs before data ever leaves the local machine.

## Architecture Context
Within the Lyne ecosystem:
* **Axis**: Localized runtime execution layer.
* **Vector**: Deterministic data stream orchestration.
* **Tangent**: Zero-trust edge inspection and credential scrubbing.

## Quickstart
Execute the core engine natively using standard python flags:
```bash
python tangent_core.py