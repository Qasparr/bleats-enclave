#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRVVTH — the audit gate as a tool: verify files against their
anchors and report the exact boundary of any disagreement.
Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice). 2026 e.v.

DOCTRINE: TRVVTH alone has absolute authority; this tool is its
clerk. It compares a file's living SHA-256 against the hash recorded
for it in the enclave chain and reports AGREE, or the zero point —
file, expected, actual — where agreement ends. It never edits,
never smooths, never rounds a mismatch into a pass.
MECHANISM: reads the CLITCOM chain (JSONL) if present; falls back to
a bare hash print when no chain exists. Exit code carries the verdict
(0 agree / 1 disagree) so scripts can gate on TRVVTH too.
93 — Live, Love, and let Love, Live.
"""
import hashlib
import json
import sys
from pathlib import Path


def sha256_of(path: Path) -> str:
    """MECHANISM: stream the file — the gate must not load a world
    into memory to weigh it."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def anchors(chain_path: Path) -> dict:
    """MECHANISM: latest anchored hash per file wins — later blocks
    supersede, and supersession is the chain's own public record."""
    found = {}
    if chain_path.exists():
        for line in chain_path.read_text().splitlines():
            if line.strip():
                blk = json.loads(line)
                found[blk["file"]] = blk["file_sha256"]
    return found


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    target = Path(sys.argv[1])
    actual = sha256_of(target)
    book = anchors(Path(
        sys.argv[2]) if len(sys.argv) > 2 else Path(
        "hidden_files/chain/chain.jsonl"))
    expected = book.get(str(target)) or book.get(str(target.resolve()))
    if expected is None:
        print(f"UNANCHORED  {target}  sha256 {actual}")
        print("no anchor on record — the gate reports, it does not pass")
        sys.exit(1)
    if expected == actual:
        print(f"AGREE       {target}  {actual[:16]}…")
        sys.exit(0)
    print(f"ZERO POINT  {target}")
    print(f"  anchored: {expected}")
    print(f"  actual:   {actual}")
    sys.exit(1)
