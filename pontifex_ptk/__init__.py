#!/usr/bin/env python3
# =============================================================================
# "Every number must show its table." — the scribe
#
# Thelemic date: Sun 2026-10-11 (dies solis), Anno V:xii e.n.
#
# 93.
#
# ptk — the PONTIFEX toolkit.
#
# A small, honest API for the four instruments of PONTIFEX reporting:
# weighing words (gematria), enciphering letters (ciphers), setting tables,
# and drawing charts. Every function is replayable: same input, same output,
# no hidden state.
#
# By Johnathan 'Qasparr' (Κασπάρρ) Monroe, Keeper of the Secret Treasure.
#
# METHOD (Scientific Illuminism): hypothesis -> method -> observation ->
# result. Each module states its doctrine up front: which tables are
# ATTESTED (handed down by the traditions) and which are CONSTRUCTED
# (built by the scribe, marked as such). Findings, never doctrine.
#
# MECHANISM: four submodules, no dependencies between them except shared
# constants. weigh.py carries the letter-number banks; cipher.py the
# substitution schemes; table.py the report tables; chart.py the figures.
#
# Live, Love, and let Love, Live. — 93.
# All Rights Reserved, Without Prejudice.
# =============================================================================

"""ptk — the PONTIFEX toolkit: weigh, cipher, table, chart."""

from . import weigh, cipher, table, chart

__version__ = "0.1.0"
__all__ = ["weigh", "cipher", "table", "chart"]

# Live, Love, and let Love, Live. — 93.
# All Rights Reserved, Without Prejudice.
