#!/usr/bin/env python3
"""Validate a wiki entry against schema.yaml.

Usage: python3 validate.py <entry.md> [--mode capture]
Exit 0 if valid, exit 1 with errors printed to stderr.
"""
import sys
import re
from pathlib import Path

WIKI_DIR = Path(__file__).parent
SCHEMA_PATH = WIKI_DIR / "schema.yaml"


def load_yaml_simple(text: str) -> dict:
    """Minimal YAML frontmatter parser — no PyYAML dependency needed.

    Handles the subset used in wiki entries: scalar strings, numbers,
    dates (YYYY-MM-DD), and bracket-delimited lists of strings.
    """
    result = {}
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("["):
            # Parse list: [a, b, c] or ["a", "b"]
            inner = value.strip("[]")
            items = [
                item.strip().strip("\"'")
                for item in re.split(r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", inner)
                if item.strip()
            ]
            result[key] = items
        else:
            result[key] = value.strip("\"'")
    return result


def extract_frontmatter(content: str) -> str | None:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None
    end = content.find("---", 3)
    if end == -1:
        return None
    return content[3:end].strip()


def extract_sections(content: str) -> list[str]:
    """Extract ## section headings from markdown content."""
    return re.findall(r"^## (.+)$", content, re.MULTILINE)


def validate(entry_path: str, mode: str = "pr") -> list[str]:
    """Validate entry, return list of error strings (empty = valid)."""
    errors = []
    path = Path(entry_path)

    if not path.exists():
        return [f"File not found: {entry_path}"]

    content = path.read_text()

    # Parse frontmatter
    fm_text = extract_frontmatter(content)
    if fm_text is None:
        return ["No YAML frontmatter found (must start with ---)"]

    fm = load_yaml_simple(fm_text)

    # Check required fields
    required_fields = ["project", "repo", "date", "author", "tags", "answers"]
    if mode == "pr":
        required_fields.extend(["pr", "branch"])

    for field in required_fields:
        if field not in fm or not fm[field]:
            errors.append(f"Missing required field: {field}")

    # Check list fields are actually lists
    list_fields = ["tags", "answers", "packages", "related"]
    for field in list_fields:
        if field in fm and not isinstance(fm[field], list):
            errors.append(f"Field '{field}' must be a list, got: {type(fm[field]).__name__}")

    # Check date format
    if "date" in fm:
        date_val = fm["date"]
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(date_val)):
            errors.append(f"Invalid date format: {date_val} (expected YYYY-MM-DD)")

    # Check required sections
    sections = extract_sections(content)
    required_sections = [
        "The problem",
        "What we did",
        "Why this way and not another",
        "What we learned",
        "Technical reference",
    ]
    for section in required_sections:
        if section not in sections:
            errors.append(f"Missing required section: ## {section}")

    return errors


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate.py <entry.md> [--mode capture]", file=sys.stderr)
        sys.exit(1)

    entry_path = sys.argv[1]
    mode = "capture" if "--mode" in sys.argv and "capture" in sys.argv else "pr"

    errors = validate(entry_path, mode)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"OK: {entry_path}")
        sys.exit(0)
