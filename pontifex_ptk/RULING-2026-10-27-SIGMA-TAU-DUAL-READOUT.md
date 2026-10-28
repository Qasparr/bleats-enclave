# RULING 2026-10-27 — The στ Dual-Readout

*A Scientific Illuminist ruling on the reporting of Greek weighings in the PONTIFEX toolkit (ptk).*

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe (Greek, -ARR, All Rights Reserved, Without Prejudice)
Tue the 27th day of October, Dies Martis, Anno V:xii e.n. (2026 e.v.)

93.

## The question

The kit's Greek bank carries the digraph 'στ' as a two-character key of value 6 — the stigma ligature. Strict letter-by-letter weighing reads the same letters apart (σ=200, τ=300). The two readings diverge on every word containing στ (11,133 entries in the Second Assault's Greek pool), and the kit reported only one number, silently. Which reading is the kit's law?

## The ruling

**Neither reading is suppressed. Where the ligature and strict weighings diverge, BOTH are reported.** (Option (c) of PEN-SHEET-2026-10-27 §3.)

- `greek(word)` keeps its historical return — the ligature value, a bare integer, so every existing call keeps working — but it now **warns** on divergence: no Greek weighing through the standard path is silently single-valued when the two witnesses disagree.
- `greek_strict(word)` weighs strictly letter by letter; the stigma sign ϛ as a written character is a letter in its own right and weighs 6 there too.
- `greek_dual(word)` returns both values as data with the divergence flagged.
- Accented letters are folded to their base letters on all Greek paths (ἀ→α, ί→ι): an accent is a reader's aid, not a letter. This corrects silent under-counts (πίστις ligature weighed 296 before the fold; it is 306). Words already stripped by callers are unaffected; every filed weighing stands.

## Delegate status

This ruling was made **by the desk under the author's trust grant** of 2026-10-27 ("If not, I trust your judgment to make the decision"), recorded in `PEN-SHEET-2026-10-27.md` §Rulings.3. It is a delegate ruling: it stands until the author's red pen revises it, and it is marked revisable wherever it is cited. The instrument is the author's; this note is the record of who moved it, when, and why.

## The type exhibit

| Word | Ligature | Strict | Note |
|---|---|---|---|
| σταυρος "cross" | **777** | **1271** | The type exhibit: the famous 777 is the ligature reading; the strict account stands beside it, neither struck |
| ἀπανίστημι | 206 | 700 | The strict reading is the slot-700 leg in the Tower's ledger |
| πίστις "faith" | 306 | 800 | The strict reading is a slot-800 alternate of record |
| θελημα | 93 | 93 | No στ: the witnesses agree; single value, no flag |
| ϛ (the sign itself) | 6 | 6 | One letter, not a fused pair; agreement |

## Verification

`calibrate()` PASS (unchanged — the banks were not touched). `selftest()` PASS: both values on στ words, single value unflagged on clean words, the ϛ case, and the standard path's warn-on-divergence / silent-on-agreement behaviour. Demonstrations printed by running `python3 -m ptk.weigh` (from `tools/`).

## Four-element test

- **Inputs:** a Greek word as written, accents welcome.
- **Processes:** fold diacritics; weigh ligature and strict; compare.
- **Outputs:** the ligature integer from `greek()` (with warning on divergence); the full pair from `greek_dual()`.
- **Tolerances:** zero — both sums are exact integer accounts of the attested bank; the bank itself was not altered by this ruling.

—

Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All Rights Reserved, Without Prejudice. Right of claim hereby reserved and coined under the authority of the Living Man.

93 — Live, Love, and let Love, Live.
