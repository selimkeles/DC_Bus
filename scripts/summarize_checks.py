#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path

OUTPUT_DIR = Path("output")


def count_violations(violations):
    errors = 0
    warnings = 0
    excluded = 0

    for violation in violations:
        if violation.get("excluded"):
            excluded += 1
        elif violation.get("severity") == "error":
            errors += 1
        elif violation.get("severity") == "warning":
            warnings += 1

    return errors, warnings, excluded


def main():
    erc = json.loads((OUTPUT_DIR / "erc.json").read_text())
    drc = json.loads((OUTPUT_DIR / "drc.json").read_text())

    erc_violations = [
        violation
        for sheet in erc.get("sheets", [])
        for violation in sheet.get("violations", [])
    ]
    drc_violations = drc.get("violations", [])

    erc_errors, erc_warnings, erc_excluded = count_violations(erc_violations)
    drc_errors, drc_warnings, drc_excluded = count_violations(drc_violations)
    unconnected = len(drc.get("unconnected_items", []))

    summary = "\n".join(
        [
            "# Design Check Summary",
            "",
            f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "## ERC",
            "",
            f"- Errors: {erc_errors}",
            f"- Warnings: {erc_warnings}",
            f"- Excluded: {erc_excluded}",
            f"- Total: {erc_errors + erc_warnings + erc_excluded}",
            "",
            "## DRC",
            "",
            f"- Errors: {drc_errors}",
            f"- Warnings: {drc_warnings}",
            f"- Excluded: {drc_excluded}",
            f"- Unconnected items: {unconnected}",
            f"- Total violations: {drc_errors + drc_warnings + drc_excluded}",
            "",
        ]
    )

    (OUTPUT_DIR / "check-summary.md").write_text(summary)
    print(summary)


if __name__ == "__main__":
    main()
