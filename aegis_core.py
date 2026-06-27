#!/usr/bin/env python3
"""
Lyne Universal Systems // Lyne Aegis Core
System Data Inspector & Security Scrub Engine
"""

import json
import re
from datetime import datetime, timezone


class AegisCore:
    def __init__(self):
        # Optimized, flexible regex engines to catch risk profiles across varying formatting
        self.risk_patterns = {
            "Cryptographic Secret Hash / Key": r"\b[0-9a-fA-F]{64}\b",
            "Exposed API Key / Token String": r"(?i)(api_key|secret|password|token|key)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-\.]{16,}\b",
            "Critical System Path Leak": r"(/|\\)(Users|home|root|etc|var)\b",
        }

    def inspect_buffer(self, raw_data: str) -> dict:
        """Parses raw text data blocks to flag structural security risks locally."""
        inspection_results = []
        lines = raw_data.splitlines()

        for line_num, line_content in enumerate(lines, 1):
            for risk_type, pattern in self.risk_patterns.items():
                if re.search(pattern, line_content):
                    # Mask the sensitive line contents instantly inside local memory
                    masked_context = (
                        line_content[:15] + "..." + line_content[-15:]
                        if len(line_content) > 30
                        else "[REDACTED BY AEGIS]"
                    )
                    inspection_results.append({
                        "line": line_num,
                        "risk_type": risk_type,
                        "flagged_context": masked_context.strip()
                    })

        return {
            "engine_status": "COMPLETED",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "metrics": {
                "lines_scanned": len(lines),
                "vulnerabilities_found": len(inspection_results)
            },
            "findings": inspection_results
        }


def main():
    print("✦ LYNE UNIVERSAL SYSTEMS // LYNE AEGIS CORE ENGINE ACTIVE")
    print("-" * 60)

    # Simulated sensitive local system log payload
    sample_system_payload = """# Initialization environment parameters
DEBUG_MODE = True
ENVIRONMENT_PATH = "/var/log/secure_auth"
APP_INTEGRATION_KEY = "secret_api_key_9876543210abcdefX"
CONNECTION_TIMEOUT = 30"""

    inspector = AegisCore()
    audit_report = inspector.inspect_buffer(sample_system_payload)

    # Output clean, schema-compliant system logs directly to standard out
    print(json.dumps(audit_report, indent=4))


if __name__ == "__main__":
    main()