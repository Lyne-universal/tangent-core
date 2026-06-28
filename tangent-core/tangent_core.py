#!/usr/bin/env python3
"""
Lyne Universal Systems // Tangent Core
System Data Inspector & Security Scrub Engine
"""

__version__ = "0.1.0"

import json
import os
import re
from datetime import datetime, timezone


class TangentEngine:

    def __init__(self):
        # TODO (Sprint 3): move patterns into patterns.py
        self.risk_patterns = {
            "Cryptographic Secret Hash / Key": r"\b[0-9a-fA-F]{64}\b",
            "Exposed API Key / Token String": r"(?i)(api_key|secret|password|token|key)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-\.]{16,}\b",
            "Critical System Path Leak": r"(/|\\)(Users|home|root|etc|var)\b",
        }

    def redact_line(self, line: str) -> tuple[str, bool]:
        """Redacts any sensitive value patterns in a single line.

        Returns:
            (redacted_line, changed)
        """
        redacted = line
        changed = False

        for risk_type, pattern in self.risk_patterns.items():
            if re.search(pattern, redacted):
                # Simple but effective redaction strategy:
                # - keep the key/left side when the secret is an assignment-like value
                # - otherwise redact the whole line
                m = re.match(r"(?i)\s*([a-zA-Z0-9_\-\.]+)\s*[:=]", redacted)
                if m:
                    key = m.group(1)
                    # replace only the right-hand sensitive value-ish segment
                    redacted = re.sub(
                        pattern,
                        f"{key}=[REDACTED]",
                        redacted,
                        flags=re.IGNORECASE,
                    )
                else:
                    redacted = re.sub(pattern, "[REDACTED]", redacted)

                # If we inserted REDACTED anywhere, consider the line changed.
                if "[REDACTED" in redacted and redacted != line:
                    changed = True

        return redacted, changed

    def process_file(self, input_file: str, output_file: str) -> dict:
        """Scans input_file line-by-line, redacts sensitive content, writes safe copy."""
        findings = []

        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        out_lines: list[str] = []
        for i, line in enumerate(lines, start=1):
            redacted_line, changed = self.redact_line(line)
            out_lines.append(redacted_line)

            if changed:
                findings.append({
                    "line": i,
                    "risk_type": "REDACTED",
                    "flagged_context": (line[:15] + "..." + line[-15:]) if len(line) > 30 else line
                })

        safe_text = "\n".join(out_lines) + ("\n" if lines else "")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(safe_text)

        return {
            "engine": "Tangent",
            "version": __version__,
            "engine_status": "COMPLETED",
            "metrics": {
                "lines_processed": len(lines),
                "vulnerabilities_neutralized": len(findings),
            },
            "output_file": output_file,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "findings": findings,
        }

    def inspect_buffer(self, raw_data: str) -> dict:
        """Backward-compatible buffer inspection (no output file)."""
        # Preserve existing external behavior by treating buffer like a file.
        pseudo_findings = []
        lines = raw_data.splitlines()

        for line_num, line_content in enumerate(lines, start=1):
            redacted_line, changed = self.redact_line(line_content)
            if changed:
                pseudo_findings.append({
                    "line": line_num,
                    "risk_type": "REDACTED",
                    "flagged_context": (line_content[:15] + "..." + line_content[-15:]) if len(line_content) > 30 else line_content,
                })

        return {
            "engine": "Tangent",
            "version": __version__,
            "engine_status": "COMPLETED",
            "metrics": {
                "lines_processed": len(lines),
                "vulnerabilities_neutralized": len(pseudo_findings),
            },
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "findings": pseudo_findings,
        }





def load_sample_env(sample_env_path: str) -> str:
    """Loads the sample env file content to be scanned by inspect_buffer."""
    with open(sample_env_path, "r", encoding="utf-8") as f:
        return f.read()


def main():

    print("Tangent Core ENGINE ACTIVE")
    print("-" * 60)

    # Load a real local sample env file and scan its contents
    sample_env_path = os.path.join(os.path.dirname(__file__), "sample.env")
    sample_system_payload = load_sample_env(sample_env_path)

    inspector = TangentEngine()
    audit_report = inspector.inspect_buffer(sample_system_payload)


    # Output clean, schema-compliant system logs directly to standard out
    print(json.dumps(audit_report, indent=4))


if __name__ == "__main__":
    main()
