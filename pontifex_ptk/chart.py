#!/usr/bin/env python3
# =============================================================================
# "Draw the number, then distrust the drawing." — the scribe
#
# Thelemic date: Sun 2026-10-11 (dies solis), Anno V:xii e.n.
#
# 93.
#
# ptk/chart.py — figures for PONTIFEX reporting, through one honest API.
#
# By Johnathan 'Qasparr' (Κασπάρρ) Monroe, Keeper of the Secret Treasure.
#
# METHOD (Scientific Illuminism): every figure is built by a function that
# takes data and a path and returns the path — no global pyplot state, no
# bare plt. calls in deliverables. A chart is replayable: same data, same
# figure, or the function is broken.
#
# MECHANISM: matplotlib with the Agg backend (no display needed — the
# figures are rendered on the headless machine). Bar charts for single
# series, grouped bars for spreads (the unity-war shape: one concept, many
# weighings), line charts for sequences. Target lines mark the numbers the
# sweep watches (77, 93, 418) — drawn as guides, never as claims.
#
# DOCTRINE: a figure illustrates a table; it never replaces one. Every
# chart function pairs with a ptk.table.Table carrying the same data.
#
# Live, Love, and let Love, Live. — 93.
# All Rights Reserved, Without Prejudice.
# =============================================================================

import matplotlib

# MECHANISM: Agg first, before pyplot import — the headless machine has no
# display, and importing pyplot first would try to find one.
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# -- The watched numbers, drawn as guide lines, never as claims ---------------
WATCHED = [77, 93, 418]


def _finish(path, title, xlabel="", ylabel=""):
    """MECHANISM: the shared finishing rite — title, labels, tight layout,
    save, close. DOCTRINE: closing the figure frees the memory; a chart
    function that leaks figures is a slow poison in a 24-worker run."""
    plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return str(path)


def bar(labels, values, path, title="", ylabel="value", watched=True,
        highlight=None):
    """MECHANISM: one bar per label. `highlight` names labels to draw in
    gold — the scribe's pen color — the rest in slate. `watched` draws the
    guide lines for 77/93/418 as dashed greys with labels, so the eye can
    check nearness without the chart claiming a hit."""
    labels = list(labels)
    values = list(values)
    assert len(labels) == len(values), "labels and values must align"
    colors = ["gold" if (highlight and l in highlight) else "slategrey"
              for l in labels]
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color=colors)
    if watched:
        for w in WATCHED:
            plt.axhline(w, color="grey", linestyle="--", linewidth=0.8)
            plt.text(len(labels) - 1, w + 2, str(w), color="grey",
                     fontsize=8)
    plt.xticks(rotation=30, ha="right")
    return _finish(path, title or "Weighings", ylabel=ylabel)


def line(xs, ys, path, title="", xlabel="x", ylabel="value", watched=True):
    """MECHANISM: a sequence joined by a line with markers — for ordered
    data (a scale walked step by step). Same guide-line doctrine as bar()."""
    xs, ys = list(xs), list(ys)
    assert len(xs) == len(ys), "xs and ys must align"
    plt.figure(figsize=(10, 5))
    plt.plot(xs, ys, marker="o", color="slategrey")
    if watched:
        for w in WATCHED:
            plt.axhline(w, color="grey", linestyle="--", linewidth=0.8)
    return _finish(path, title or "Sequence", xlabel=xlabel, ylabel=ylabel)


def spread(data, path, title="", ylabel="value"):
    """MECHANISM: the unity-war shape — one group of bars per concept, one
    bar per weighing in the group. `data` maps concept -> list of values
    (the spread). DOCTRINE: the spread is the honest figure — it shows every
    weighing, so no single number gets to pretend it is the answer."""
    concepts = list(data.keys())
    series = [list(data[c]) for c in concepts]
    width = max(len(s) for s in series)
    n = len(concepts)
    plt.figure(figsize=(max(10, n * 1.6), 5))
    x = range(n)
    palette = ["slategrey", "gold", "darkgrey", "peru"]
    for i in range(width):
        vals = [s[i] if i < len(s) else 0 for s in series]
        offs = [p + (i - width / 2 + 0.5) * 0.8 / max(width, 1) for p in x]
        plt.bar(offs, vals, width=0.8 / max(width, 1),
                color=palette[i % len(palette)],
                label=f"weighing {i + 1}" if width > 1 else None)
    if width > 1:
        plt.legend(fontsize=8)
    plt.xticks(list(x), concepts, rotation=30, ha="right")
    for w in WATCHED:
        plt.axhline(w, color="grey", linestyle="--", linewidth=0.8)
        plt.text(n - 1, w + 3, str(w), color="grey", fontsize=8)
    return _finish(path, title or "Spreads", ylabel=ylabel)


# Live, Love, and let Love, Live. — 93.
# All Rights Reserved, Without Prejudice.
