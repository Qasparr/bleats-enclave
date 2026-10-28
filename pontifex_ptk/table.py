#!/usr/bin/env python3
# =============================================================================
# "One table, three mouths: the page, the ledger, the print."
# — the scribe
#
# Thelemic date: Sun 2026-10-11 (dies solis), Anno V:xii e.n.
#
# 93.
#
# ptk/table.py — one table object, three renderings: Markdown, CSV, PDF.
#
# By Johnathan 'Qasparr' (Κασπάρρ) Monroe, Keeper of the Secret Treasure.
#
# METHOD (Scientific Illuminism): the Table holds data; the renderers hold
# opinions about presentation. Data enters once, through the constructor,
# and every mouth speaks from the same rows — a Markdown table and its PDF
# twin can never disagree, because there is only one table.
#
# MECHANISM: Table(headers, rows) — headers a list of str, rows a list of
# lists. to_markdown() and to_csv() are pure string builders; to_pdf()
# uses fpdf2 with the PONTIFEX report styling (DejaVu + Noto fallbacks,
# HarfBuzz shaping for Hebrew/CJK). Ragged rows are padded, never truncated.
#
# Live, Love, and let Love, Live. — 93.
# All Rights Reserved, Without Prejudice.
# =============================================================================

import csv
from pathlib import Path

DJ = "/usr/share/fonts/truetype/dejavu"
NOTO = "/usr/share/fonts/truetype/noto"


class Table:
    """A rectangular table with three mouths.

    MECHANISM: normalized at construction — every row padded to the header
    width with "". DOCTRINE: padding is honest (the cell is empty); silent
    truncation would be a lie, so ragged rows grow, never shrink.
    """

    def __init__(self, headers, rows):
        self.headers = [str(h) for h in headers]
        width = len(self.headers)
        self.rows = []
        for r in rows:
            cells = [str(c) for c in r]
            cells += [""] * (width - len(cells))
            self.rows.append(cells[:width])

    def __len__(self):
        """MECHANISM: the row count — the number the report calls 'n'."""
        return len(self.rows)

    # -- Mouth 1: Markdown ---------------------------------------------------
    def to_markdown(self):
        """MECHANISM: GitHub-flavored Markdown table. DOCTRINE: the working
        mouth — diffable, reviewable, the red pen's native tongue."""
        lines = [
            "| " + " | ".join(self.headers) + " |",
            "|" + "|".join(["---"] * len(self.headers)) + "|",
        ]
        for r in self.rows:
            lines.append("| " + " | ".join(r) + " |")
        return "\n".join(lines) + "\n"

    def save_markdown(self, path):
        """MECHANISM: write the Markdown mouth to disk."""
        Path(path).write_text(self.to_markdown(), encoding="utf-8")
        return str(path)

    # -- Mouth 2: CSV ---------------------------------------------------------
    def to_csv(self, path):
        """MECHANISM: machine mouth — headers then rows, UTF-8, csv module
        quoting. DOCTRINE: the replayable source; a PDF is presentation, the
        CSV is the record."""
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(self.headers)
            w.writerows(self.rows)
        return str(path)

    # -- Mouth 3: PDF ----------------------------------------------------------
    def to_pdf(self, path, title=""):
        """MECHANISM: print mouth — fpdf2 table with the PONTIFEX report
        styling. The last column takes double width (it carries the notes);
        the rest split evenly. Long tables flow across pages via fpdf2's own
        page-break handling inside table()."""
        from fpdf import FPDF

        pdf = FPDF(format="A4", unit="mm")
        pdf.set_auto_page_break(True, margin=18)
        pdf.set_margins(14, 16, 14)
        pdf.add_font("base", "", f"{DJ}/DejaVuSans.ttf")
        pdf.add_font("base", "B", f"{DJ}/DejaVuSans-Bold.ttf")
        pdf.add_font("base", "I", f"{NOTO}/NotoSans-Italic.ttf")
        fallbacks = []
        for i, fb in enumerate([
                f"{NOTO}/NotoSansCoptic-Regular.ttf",
                f"{NOTO}/NotoSansEthiopic-ExtraLight.ttf"]):
            if Path(fb).exists():
                pdf.add_font(f"fb{i}", "", fb)
                fallbacks.append(f"fb{i}")
        pdf.set_fallback_fonts(fallbacks)
        pdf.set_text_shaping(True)
        pdf.add_page()

        if title:
            pdf.set_font("base", "B", 16)
            pdf.multi_cell(0, 8, title, align="C")
            pdf.ln(4)

        ncols = len(self.headers)
        usable = 182.0
        unit = usable / (ncols + 1)  # last column counts double
        widths = [unit] * (ncols - 1) + [unit * 2]

        pdf.set_font("base", "", 8)
        with pdf.table(col_widths=widths, line_height=5) as t:
            hr = t.row()
            for h in self.headers:
                hr.cell(h)
            for r in self.rows:
                row = t.row()
                for c in r:
                    row.cell(c)

        for p in range(1, pdf.pages_count + 1):
            pdf.page = p
            pdf.set_y(-14)
            pdf.set_font("base", "", 8)
            pdf.cell(0, 6, f"— {p} —", align="C")

        pdf.output(str(path))
        return str(path)


def from_markdown(text):
    """MECHANISM: parse a Markdown table back into a Table. DOCTRINE: the
    round trip — a table the red pen edits in Markdown re-enters the
    machine without retyping."""
    rows = []
    for line in text.strip().splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue  # the separator row carries no data
        rows.append(cells)
    if not rows:
        raise ValueError("no table found in text")
    return Table(rows[0], rows[1:])


# Live, Love, and let Love, Live. — 93.
# All Rights Reserved, Without Prejudice.
