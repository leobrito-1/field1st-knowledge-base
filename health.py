#!/usr/bin/env python3
"""Hidden maintenance checks for the local wiki.

This script is intended to run after `/wiki` saves an entry. It validates
canonical raw-entry rules and reports actionable issues without changing files.
Exit 1 only for structural errors that need attention; warnings keep exit 0.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from validate import validate as validate_entry

WIKI_DIR = Path(__file__).parent
RAW_DIR = WIKI_DIR / "raw"
LOG_PATH = WIKI_DIR / "log.md"
GRAPH_DIR = WIKI_DIR / "graphify-out"
FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$")
LOG_ENTRY_RE = re.compile(r"\[raw/([^\]]+\.md)\]")


def check_filename_policy(paths) -> list[str]:
    errors: list[str] = []
    for path in sorted(paths, key=lambda p: p.name):
        if not FILENAME_RE.match(path.name):
            errors.append(
                "Raw file does not match YYYY-MM-DD-short-description.md: "
                f"{path.name}"
            )
    return errors


def entry_mode(path: Path) -> str:
    text = path.read_text()
    if re.search(r"^pr:\s*", text, re.MULTILINE) and re.search(r"^branch:\s*", text, re.MULTILINE):
        return "pr"
    return "capture"


def check_raw_validation(raw_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(raw_dir.glob("*.md")):
        for message in validate_entry(str(path), mode=entry_mode(path)):
            errors.append(f"{path.name}: {message}")
    return errors


def check_log_consistency(raw_dir: Path, log_path: Path) -> tuple[list[str], list[str]]:
    if not log_path.exists():
        return ["Missing log.md"], []

    log_text = log_path.read_text()
    referenced = {match.group(1) for match in LOG_ENTRY_RE.finditer(log_text)}
    raw_names = {path.name for path in raw_dir.glob("*.md")}

    errors = [
        f"Log references missing raw file: {name}"
        for name in sorted(referenced - raw_names)
    ]
    warnings = [
        f"Raw file is not indexed in log.md: {name}"
        for name in sorted(raw_names - referenced)
    ]
    return errors, warnings


def check_graph_staleness(raw_dir: Path, graph_dir: Path) -> list[str]:
    raw_files = list(raw_dir.glob("*.md"))
    if not raw_files or not graph_dir.exists():
        return []

    derived_files = [path for path in graph_dir.rglob("*") if path.is_file()]
    if not derived_files:
        return ["graphify-out exists but has no generated files"]

    newest_raw = max(path.stat().st_mtime for path in raw_files)
    newest_graph = max(path.stat().st_mtime for path in derived_files)
    if newest_raw > newest_graph:
        return ["graphify-out is stale relative to raw/; run graphify --update"]
    return []


def run_health_check(wiki_dir: Path = WIKI_DIR) -> tuple[list[str], list[str]]:
    raw_dir = wiki_dir / "raw"
    errors = []
    warnings = []

    errors.extend(check_filename_policy(raw_dir.glob("*.md")))
    errors.extend(check_raw_validation(raw_dir))

    log_errors, log_warnings = check_log_consistency(raw_dir, wiki_dir / "log.md")
    errors.extend(log_errors)
    warnings.extend(log_warnings)

    warnings.extend(check_graph_staleness(raw_dir, wiki_dir / "graphify-out"))
    return errors, warnings


def main() -> int:
    errors, warnings = run_health_check()

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")

    if errors:
        return 1

    print("OK: wiki health check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
