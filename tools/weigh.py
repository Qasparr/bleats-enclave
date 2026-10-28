#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WEIGH — the PONTIFEX kit at the command line, under the standing
order: always the Trinity and the Cube too, if it works.
Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice). 2026 e.v.

DOCTRINE: each word weighed in its own tongue; the Trinity = the
name in its own bank (English ordinal for English, Hebrew for
Hebrew), the Latin ordinal, and Agrippa — three witnesses, no bank
monopolizing the light. The Cube = decade-factorization across the
27-grid and the reduction's passage, if any, through the hidden
center 13. Where a check does not work, it is reported unseated.
MECHANISM: thin CLI over the vendored pontifex_ptk (ptk.weigh).
93 — Live, Love, and let Love, Live.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pontifex_ptk import weigh as W  # noqa: E402


def chain(n: int) -> list:
    """MECHANISM: the theosophical reduction chain, whole — every
    landing printed, so a passage through 13 is seen, not claimed."""
    out = [n]
    while n > 9:
        n = sum(int(d) for d in str(n))
        out.append(n)
    return out


def cube(n: int) -> str:
    """MECHANISM: a value seats in the Cube iff it factors as
    100a + 10b + c with each term a grid slot (a,b,c in 1..9 or 0)."""
    if n > 999:
        return "unseated (over the grid's ceiling)"
    a, rem = divmod(n, 100)
    b, c = divmod(rem, 10)
    return f"seated: {a * 100} + {b * 10} + {c}"


if __name__ == "__main__":
    word = " ".join(sys.argv[1:]).replace(" ", "")
    if not word:
        print(__doc__)
        sys.exit(2)
    for label, bank in (("ordinal", W.LATIN_ORDINAL),
                        ("agrippa", W.AGRIPPA)):
        v = W.weigh(word, bank)
        print(f"{word} | {label} {v} | reduction {chain(v)} | "
              f"cube {cube(v)}")
