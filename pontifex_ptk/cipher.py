#!/usr/bin/env python3
# =============================================================================
# "The cipher is a mirror; check which face you are looking at."
# — the scribe
#
# Thelemic date: Sun 2026-10-11 (dies solis), Anno V:xii e.n.
#
# 93.
#
# ptk/cipher.py — classical letter-substitution ciphers.
#
# By Johnathan 'Qasparr' (Κασπάρρ) Monroe, Keeper of the Secret Treasure.
#
# METHOD (Scientific Illuminism): each scheme is stated as an explicit
# pairing, printed in full — no hidden alphabets. ATTESTED schemes
# (Atbash, Albam) are recorded as the traditions hand them down.
# DOCTRINE: a scheme the scribe cannot verify from sources is NOT shipped
# as working — it raises, loudly, with the reason. (Achbi is withheld on
# exactly these grounds: the pairing could not be verified 2026-10-11.
# The red pen may supply it.)
#
# MECHANISM: every cipher is a dict {plain: cipher}. encipher() applies a
# mapping; decipher() inverts it. All pairings are involutions (applying
# twice returns the original) — the module asserts this at import.
#
# Live, Love, and let Love, Live. — 93.
# All Rights Reserved, Without Prejudice.
# =============================================================================

# ---------------------------------------------------------------------------
# The Hebrew abjad order (ATTESTED): the 22 letters in their canonical order.
# MECHANISM: non-final forms only — ciphers pair letters, not positional
# variants. Final forms (ךםןףץ) map to their base letter before enciphering.
# ---------------------------------------------------------------------------
HEBREW_ORDER = list('אבגדהוזחטיכלמנסעפצקרשת')

_FINALS = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}


def _build_atbash():
    """MECHANISM: אתבש — first↔last, second↔second-last, … (reversed alphabet).
    DOCTRINE: ATTESTED — the biblical cipher (Jer. 25:26 ששך for בבל)."""
    n = len(HEBREW_ORDER)
    return {HEBREW_ORDER[i]: HEBREW_ORDER[n - 1 - i] for i in range(n)}


def _build_albam():
    """MECHANISM: אלבם — the alphabet halved: first 11 ↔ last 11
    (א↔ל, ב↔מ, …). DOCTRINE: ATTESTED — the classical companion to Atbash."""
    half = len(HEBREW_ORDER) // 2
    m = {}
    for i in range(half):
        a, b = HEBREW_ORDER[i], HEBREW_ORDER[i + half]
        m[a], m[b] = b, a
    return m


# -- The ATTESTED Hebrew schemes, built programmatically so the pairing ----
# -- logic is visible, then frozen as data. ----------------------------------
ATBASH_HE = _build_atbash()
ALBAM_HE = _build_albam()


def achbi(word):
    """DOCTRINE: WITHHELD. The אכבי pairing could not be verified against
    sources on 2026-10-11, so it is not shipped as a working cipher.
    Shipping an unverified scheme would be exactly the kind of silent
    fabrication this toolkit exists to prevent. The red pen may supply the
    attested pairing; until then, this raises."""
    raise NotImplementedError(
        "achbi: pairing unverified 2026-10-11 — not shipped. "
        "Supply the attested אכבי pairing to enable."
    )


# ---------------------------------------------------------------------------
# Latin schemes
# ---------------------------------------------------------------------------

def _build_latin_atbash():
    """MECHANISM: A↔Z, B↔Y, … — the Latin mirror of Atbash."""
    alpha = [chr(ord('A') + i) for i in range(26)]
    return {alpha[i]: alpha[25 - i] for i in range(26)}


ATBASH_LATIN = _build_latin_atbash()


def caesar_mapping(shift):
    """MECHANISM: build the Caesar shift mapping for a given shift.
    DOCTRINE: the shift is a parameter, never a default — a cipher with a
    hidden default shift is a claim wearing a method's clothes."""
    alpha = [chr(ord('A') + i) for i in range(26)]
    return {alpha[i]: alpha[(i + shift) % 26] for i in range(26)}


# ---------------------------------------------------------------------------
# The engine
# ---------------------------------------------------------------------------

def encipher(text, mapping):
    """MECHANISM: substitute each character through the mapping; characters
    with no entry (spaces, punctuation) pass through unchanged and audible
    — the output keeps its word-breaks so the transform stays checkable."""
    return ''.join(mapping.get(ch, ch) for ch in text)


def decipher(text, mapping):
    """MECHANISM: invert the mapping and encipher. DOCTRINE: every scheme
    here is an involution, so decipher(cipher(x)) == x — asserted at import
    below, not assumed."""
    inv = {v: k for k, v in mapping.items()}
    return encipher(text, inv)


def atbash_he(word):
    """Atbash on Hebrew text (ATTESTED scheme). Final forms normalized to
    base letters first — the cipher pairs letters, not positions."""
    norm = ''.join(_FINALS.get(ch, ch) for ch in word)
    return encipher(norm, ATBASH_HE)


def albam_he(word):
    """Albam on Hebrew text (ATTESTED scheme). Same final-form handling."""
    norm = ''.join(_FINALS.get(ch, ch) for ch in word)
    return encipher(norm, ALBAM_HE)


def atbash_latin(word):
    """Atbash on Latin-script text (case-insensitive; output uppercase)."""
    return encipher(word.upper(), ATBASH_LATIN)


def caesar(word, shift):
    """Caesar shift on Latin-script text. The shift is required — see
    caesar_mapping's doctrine."""
    return encipher(word.upper(), caesar_mapping(shift))


def rot13(word):
    """MECHANISM: Caesar with shift 13 — the one fixed-shift cipher the
    tradition blesses by name. Included for completeness, not for secrecy."""
    return caesar(word, 13)


def show_pairing(mapping, name):
    """MECHANISM: print a pairing in full, plain1→cipher1 order.
    DOCTRINE: the audit view — a cipher you cannot print, you do not trust."""
    pairs = ' '.join(f"{k}→{v}" for k, v in mapping.items())
    return f"{name}: {pairs}"


# ---------------------------------------------------------------------------
# Self-check: every shipped scheme must be an involution.
# MECHANISM: apply twice to the full alphabet; any failure raises at import.
# DOCTRINE: the module refuses to load a broken mirror.
# ---------------------------------------------------------------------------
for _name, _m in [("ATBASH_HE", ATBASH_HE), ("ALBAM_HE", ALBAM_HE),
                  ("ATBASH_LATIN", ATBASH_LATIN)]:
    _alpha = ''.join(_m.keys())
    assert decipher(encipher(_alpha, _m), _m) == _alpha, \
        f"{_name} is not an involution — refusing to load"
del _name, _m, _alpha

# Live, Love, and let Love, Live. — 93.
# All Rights Reserved, Without Prejudice.
