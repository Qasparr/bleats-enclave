#!/usr/bin/env python3
# =============================================================================
# "Weigh the word in its own tongue." — the scribe
#
# Thelemic date: Sun 2026-10-11 (dies solis), Anno V:xii e.n.
#
# 93.
#
# ptk/weigh.py — letter-number weighing (gematria / isopsephy / abjad).
#
# By Johnathan 'Qasparr' (Κασπάρρ) Monroe, Keeper of the Secret Treasure.
#
# METHOD (Scientific Illuminism): the tables below are ATTESTED copies of
# pontifex/pontifex/tables.py as of 2026-10-11 — the traditions hand them
# down; the scribe does not "improve" them. DOCTRINE: if a table ever needs
# correction, correct it in pontifex and re-sync here; never edit the copy
# silently. Anything the scribe builds (mispar gadol finals are standard,
# but the *convenience wrappers* are his) is marked where registered.
#
# MECHANISM: each bank is a plain dict {letter: value}. weigh() sums a word
# letter by letter, ignoring characters the bank does not know (spaces,
# punctuation, vowel points) — loudly: unknown() reports what was skipped,
# so no weighing ever silently drops a letter.
#
# Live, Love, and let Love, Live. — 93.
# All Rights Reserved, Without Prejudice.
# =============================================================================

# MECHANISM: unicodedata folds Greek diacritics for the dual-readout path
# (see greek_strict below); warnings carries the divergence note the
# 2026-10-27 ruling requires in the standard path. No other dependencies —
# the kit stays bare-metal on purpose.
import unicodedata
import warnings

# ---------------------------------------------------------------------------
# DOCTRINE: provenance. ATTESTED copies of pontifex/pontifex/tables.py,
# synced 2026-10-11. The scribe records; he does not revise.
# ---------------------------------------------------------------------------

# -- Hebrew, mispar hechrechi (ATTESTED) ------------------------------------
# MECHANISM: the standard values; final forms (ךםןףץ) share their letter's
# value in this bank. Root engine of the correspondences.
HEBREW = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50,
    'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100,
    'ר': 200, 'ש': 300, 'ת': 400,
}

# -- Hebrew, mispar gadol finals (ATTESTED as the standard convention) ------
# MECHANISM: in the "great numbering" the five final forms take the hundreds
# beyond ת: ך=500, ם=600, ן=700, ף=800, ץ=900. This is what made אעם=671 in
# the G-1 verification — the print itself flagged the final-mem valuation.
HEBREW_GADOL_FINALS = {'ך': 500, 'ם': 600, 'ן': 700, 'ף': 800, 'ץ': 900}

# -- Greek, Milesian isopsephy (ATTESTED) -----------------------------------
# MECHANISM: classical values; the three epissemones (ϛ=6, ϟ=90, ϡ=900)
# included because the classical system needs them.
GREEK = {
    'α': 1, 'β': 2, 'γ': 3, 'δ': 4, 'ε': 5, 'ϛ': 6, 'στ': 6, 'ζ': 7,
    'η': 8, 'θ': 9, 'ι': 10, 'κ': 20, 'λ': 30, 'μ': 40, 'ν': 50, 'ξ': 60,
    'ο': 70, 'π': 80, 'ϟ': 90, 'ρ': 100, 'σ': 200, 'ς': 200, 'τ': 300,
    'υ': 400, 'φ': 500, 'χ': 600, 'ψ': 700, 'ω': 800, 'ϡ': 900,
}

# -- Latin / English ordinal, A=1..Z=26 (ATTESTED as the working table) -----
# MECHANISM: the plain ordinal. DOCTRINE: this is what "Latin gematria" is
# in practice — the scale English words are weighed on (CELL=32, AXONEME=77).
LATIN_ORDINAL = {chr(ord('A') + i): i + 1 for i in range(26)}

# -- Latin, Agrippa's table, De occulta philosophia II.xix (ATTESTED) --------
# MECHANISM: Agrippa's published values; J read as I, U as V, per the
# classical alphabet he worked in. The scribe records, not revises.
AGRIPPA = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
    'I': 9, 'J': 9, 'K': 10, 'L': 20, 'M': 30, 'N': 40, 'O': 50, 'P': 60,
    'Q': 70, 'R': 80, 'S': 90, 'T': 100, 'U': 200, 'V': 200, 'X': 300,
    'Y': 400, 'Z': 500,
}

# -- Arabic, abjad numerals, Eastern order (ATTESTED) ------------------------
# MECHANISM: the traditional abjadī order values. (The Maghrebi order differs
# in a few letters; the Eastern order is recorded and the difference noted,
# not hidden.)
ARABIC_ABJAD = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8,
    'ط': 9, 'ي': 10, 'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60,
    'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400,
    'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000,
}


# ---------------------------------------------------------------------------
# The engine
# ---------------------------------------------------------------------------

def weigh(word, bank):
    """MECHANISM: sum the values of every character the bank knows.

    DOCTRINE: characters the bank does not know (spaces, punctuation,
    vowel points, maqaf) contribute 0 — they are separators, not letters.
    Use unknown() to audit what was skipped; a weighing is only honest if
    its skips are visible.
    """
    return sum(bank.get(ch, 0) for ch in word)


def unknown(word, bank):
    """MECHANISM: report the characters weigh() skipped, in order of first
    appearance. DOCTRINE: the audit trail. Call this whenever a weighing
    surprises you — the surprise is usually here."""
    seen, out = set(), []
    for ch in word:
        if ch not in bank and ch not in seen:
            seen.add(ch)
            out.append(ch)
    return out


def breakdown(word, bank):
    """MECHANISM: the letter-by-letter accounting: [(letter, value), ...]
    plus the total. DOCTRINE: show your work — a bare number proves nothing;
    the breakdown lets the red pen check every letter."""
    pairs = [(ch, bank[ch]) for ch in word if ch in bank]
    return pairs, sum(v for _, v in pairs)


def hebrew(word):
    """Weigh a Hebrew word in mispar hechrechi (ATTESTED bank)."""
    return weigh(word, HEBREW)


def hebrew_gadol(word):
    """MECHANISM: mispar gadol — as hebrew(), but the five final forms take
    their great values (ך=500 … ץ=900). DOCTRINE: the bank must be NAMED in
    the report; hechrechi and gadol are different weighings of the same word,
    and conflating them is how phantom discrepancies are born."""
    total = 0
    for ch in word:
        if ch in HEBREW_GADOL_FINALS:
            total += HEBREW_GADOL_FINALS[ch]
        else:
            total += HEBREW.get(ch, 0)
    return total


def _fold_greek(word):
    """MECHANISM: normalise a Greek word for weighing — lowercase, then
    strip diacritics (breathings, tonos, diaeresis) by NFD decomposition,
    dropping combining marks, and recomposing. ἀ→α, ί→ι, ή→η.

    DOCTRINE: an accent is a reader's aid, not a letter; a weighing that
    silently skips an accented vowel under-counts the word. Before
    2026-10-27 the kit skipped accented letters whole (πίστις weighed
    296 ligature instead of 306). Folding makes the skip visible as a
    correction, recorded here — never silent. Words already stripped by
    the caller are unchanged by the fold, so every filed weighing stands.
    """
    decomposed = unicodedata.normalize('NFD', word.lower())
    stripped = ''.join(ch for ch in decomposed
                       if unicodedata.category(ch) != 'Mn')
    return unicodedata.normalize('NFC', stripped)


def greek_strict(word):
    """Weigh a Greek word STRICTLY letter by letter (Milesian values).

    MECHANISM: fold diacritics (see _fold_greek), then sum single letters
    only — σ=200 and τ=300 are always counted apart; the digraph is never
    fused. The stigma SIGN ϛ, where a text carries it as one character,
    is a letter in its own right and weighs 6 in this mode too.

    DOCTRINE: this is the second witness the 2026-10-27 dual-readout
    ruling (RULING-2026-10-27-SIGMA-TAU-DUAL-READOUT.md, delegate ruling,
    revisable by the author's pen) requires beside the ligature reading:
    neither reading is the "true" one by decree — both are reported.
    """
    w = _fold_greek(word)
    return sum(GREEK[ch] for ch in w if len(ch) == 1 and ch in GREEK)


def greek(word):
    """Weigh a Greek word in Milesian isopsephy (ATTESTED bank) — the
    LIGATURE reading: the στ digraph counts as stigma, 6.

    MECHANISM: fold diacritics, lowercase (the bank is keyed on lowercase
    with epissemones); 'στ' is handled as a two-character key, so check it
    before single letters.

    DOCTRINE (ruling 2026-10-27): where the ligature reading and the
    strict letter-by-letter reading (greek_strict) diverge, this function
    still returns the ligature value — the historical default — but it
    WARNS: no Greek weighing through the standard path is silently
    single-valued when the two witnesses disagree. Use greek_dual() to
    receive both numbers as data."""
    w = _fold_greek(word)
    total, i = 0, 0
    while i < len(w):
        if w[i:i + 2] == 'στ':
            total += 6
            i += 2
        else:
            total += GREEK.get(w[i], 0)
            i += 1
    strict = greek_strict(word)
    if strict != total:
        warnings.warn(
            "στ dual-readout: %r weighs %d (ligature) / %d (strict) — "
            "both readings stand; see greek_dual()" % (word, total, strict),
            UserWarning, stacklevel=2)
    return total


def greek_dual(word):
    """MECHANISM: the dual readout ruled 2026-10-27 — weigh a Greek word
    BOTH ways and return the pair as data:
        {'word', 'ligature', 'strict', 'divergent', 'note'}
    'ligature' is greek()'s στ-as-stigma value (without its warning —
    this function IS the place the divergence is surfaced, so it reads
    the ligature sum directly); 'strict' is greek_strict(); 'divergent'
    is True exactly when the two witnesses disagree.

    DOCTRINE: a divergence is a finding, not an error to be repaired by
    choosing a winner. Type exhibit, filed in the ruling note:
    σταυρος — 777 ligature / 1271 strict.

    Inputs:  the word as written (accents welcome; they are folded).
    Outputs: the dict above; neither value is ever suppressed.
    Tolerances: zero — both sums are exact integer accounts of the bank.
    """
    w = _fold_greek(word)
    ligature, i = 0, 0
    while i < len(w):
        if w[i:i + 2] == 'στ':
            ligature += 6
            i += 2
        else:
            ligature += GREEK.get(w[i], 0)
            i += 1
    strict = greek_strict(word)
    divergent = ligature != strict
    return {
        'word': word,
        'ligature': ligature,
        'strict': strict,
        'divergent': divergent,
        'note': ('στ dual-readout: both readings stand'
                 if divergent else 'readings agree'),
    }


def latin(word):
    """Weigh a Latin-script word in ordinal A=1..Z=26 (ATTESTED bank).

    MECHANISM: case-insensitive; non-letters skipped (see unknown())."""
    return weigh(word.upper(), LATIN_ORDINAL)


def agrippa(word):
    """Weigh a Latin-script word in Agrippa's table (ATTESTED bank)."""
    return weigh(word.upper(), AGRIPPA)


def arabic(word):
    """Weigh an Arabic word in abjad numerals, Eastern order (ATTESTED)."""
    return weigh(word, ARABIC_ABJAD)


def calibrate():
    """MECHANISM: the anchorage. Weigh the calibration words every bank must
    reproduce; raise AssertionError on any failure.

    DOCTRINE: nothing enters the work unverified — including this module.
    Run calibrate() before any weighing session. עז=77 is the scribe's own
    name-word; THELEMA=AGAPE=93 the Greek-bank convergence; AXONEME=77 the
    English-ordinal bridge.
    """
    checks = [
        (hebrew('עז'), 77, "HEBREW עז"),
        (greek('θελημα'), 93, "GREEK θελημα"),
        (greek('αγαπη'), 93, "GREEK αγαπη"),
        (latin('AXONEME'), 77, "LATIN AXONEME"),
        (latin('CELL'), 32, "LATIN CELL"),
        (hebrew_gadol('אעם'), 671, "GADOL אעם"),
    ]
    for got, want, name in checks:
        assert got == want, f"calibration failed: {name} = {got}, want {want}"
    return True


def selftest():
    """MECHANISM: the στ dual-readout checks ruled 2026-10-27, beside the
    anchorage above. calibrate() guards the banks; selftest() guards the
    READINGS. Raise AssertionError on any failure; return True on pass.

    The cases, one per clause of the ruling:
    (1) a στ word reports BOTH values — σταυρος 777 ligature / 1271
        strict, divergent flagged (the type exhibit);
    (2) accented στ words fold and report both — ἀπανίστημι 206 / 700,
        πίστις 306 / 800;
    (3) a word with no στ stays single-valued, unflagged — θελημα 93;
    (4) the stigma sign ϛ itself weighs 6 under both readings — the sign
        is one letter, not a fused pair, so the witnesses agree;
    (5) the standard path warns on divergence and stays silent on
        agreement — no silent single value, no noise without cause.
    """
    import warnings as _warnings

    dual = greek_dual('σταυρος')
    assert (dual['ligature'], dual['strict'], dual['divergent']) \
        == (777, 1271, True), f"σταυρος dual failed: {dual}"
    dual = greek_dual('ἀπανίστημι')
    assert (dual['ligature'], dual['strict'], dual['divergent']) \
        == (206, 700, True), f"ἀπανίστημι dual failed: {dual}"
    dual = greek_dual('πίστις')
    assert (dual['ligature'], dual['strict'], dual['divergent']) \
        == (306, 800, True), f"πίστις dual failed: {dual}"
    dual = greek_dual('θελημα')
    assert (dual['ligature'], dual['strict'], dual['divergent']) \
        == (93, 93, False), f"θελημα dual failed: {dual}"
    dual = greek_dual('ϛ')
    assert (dual['ligature'], dual['strict'], dual['divergent']) \
        == (6, 6, False), f"ϛ dual failed: {dual}"
    assert greek_strict('ϛ') == 6 and greek('ϛ') == 6
    with _warnings.catch_warnings(record=True) as caught:
        _warnings.simplefilter('always')
        assert greek('σταυρος') == 777
        assert len(caught) == 1 and 'dual-readout' in str(caught[0].message), \
            "standard path must warn exactly once on a divergent weighing"
    with _warnings.catch_warnings(record=True) as caught:
        _warnings.simplefilter('always')
        assert greek('θελημα') == 93
        assert len(caught) == 0, \
            "standard path must stay silent when the readings agree"
    return True


if __name__ == '__main__':
    # MECHANISM: running the module directly runs the anchorage, then the
    # dual-readout self-test, then prints the ruled demonstrations.
    # DOCTRINE: an instrument that cannot show its papers on demand is
    # not an instrument.
    calibrate()
    selftest()
    print('calibrate: PASS · selftest (στ dual-readout): PASS')
    for demo in ('σταυρος', 'ἀπανίστημι', 'πίστις', 'θελημα'):
        d = greek_dual(demo)
        print('%s -> ligature %d · strict %d · divergent %s'
              % (demo, d['ligature'], d['strict'], d['divergent']))


# Live, Love, and let Love, Live. — 93.
# All Rights Reserved, Without Prejudice.
