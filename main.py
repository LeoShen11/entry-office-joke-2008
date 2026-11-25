#!/usr/bin/env python3
"""One-Line Office Joke Laugh-Off entry.

Writes a single original one-line office joke to $MAKEFUN_OUTPUT_DIR/entry.txt
and validates it against the gate: UTF-8 text, 1 to 200 characters, one line,
not only whitespace.
"""

import os
import sys

JOKE = (
    "The office printer only jams on urgent documents — "
    "it's the most honest performance review in the building."
)

MAX_CHARS = 200


def validate(text: str) -> None:
    """Raise if the joke breaks any gate rule."""
    if not text:
        raise ValueError("joke is empty")
    if text != text.strip():
        raise ValueError("joke has leading or trailing whitespace")
    if not text.strip():
        raise ValueError("joke is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"joke is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    words = text.split()
    if len(words) < 5 or len(words) > 35:
        raise ValueError(f"joke has {len(words)} words, expected 5-35")


def main() -> int:
    validate(JOKE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(JOKE)

    # Read-back check: the file on disk must be exactly the joke, byte for byte.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != JOKE:
        raise ValueError("read-back mismatch: entry.txt differs from the joke")
    if len(written) != len(JOKE):
        raise ValueError("read-back length mismatch")

    print(f"wrote {len(JOKE)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
