#!/usr/bin/env python3
"""Two Days of Quiet Dread — make.fun entry.

Writes one single-line code review comment to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt). The comment approves a pull
request while carrying quiet existential dread, in the flat voice
of a tired engineer clicking approve.
"""

import os
import sys

# Grader runs `python3 -P -s main.py`: -P keeps the script dir off
# sys.path, so bootstrap it here before any local import.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# The entry: one line, 91 characters, no trailing newline in the file.
ENTRY_TEXT = (
    "Approved. Somewhere in this diff is the bug that ends us; "
    "it is not my job to find it today."
)

MAX_CHARS = 140


def validate(text):
    """Gate mirror: UTF-8, 1-140 chars, single line, not only whitespace."""
    if not text.strip():
        raise SystemExit("entry must not be blank")
    if len(text) > MAX_CHARS:
        raise SystemExit("entry exceeds 140 characters")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    text.encode("utf-8")  # raises on non-UTF-8, matching the sealed scorer


def write_entry(text, out_dir):
    """Write atomically so a partial run never leaves a half file."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, path)
    return path


def main():
    validate(ENTRY_TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    path = write_entry(ENTRY_TEXT, out_dir)
    # Read back and confirm the file holds exactly the entry, byte for byte.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != ENTRY_TEXT:
        raise SystemExit("read-back mismatch: entry.txt differs from ENTRY_TEXT")
    print(f"wrote {len(ENTRY_TEXT)} chars to {path}")


if __name__ == "__main__":
    main()
