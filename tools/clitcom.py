#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLITCOM — Command Line Interface Terminvs
"First, implode and then explode, I am combustible." — Krizz Kaliko,
'Dysfunctional', 2009 (the Hip-Hop Well of the parent instrument)

Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice).
XXVIII day of October, 2026 e.v. — Method of Science, Aim of Religion.

DOCTRINE: CLITCOM is the terminus of the sovereign layer built for the
Biosensory Catalyst Module: DNS REGISTRAR (names -> onion roots),
HOST (the static mirror), and CHAIN-KEEPER (the hash-chained anchor
ledger). One terminal, three offices, per the author's charter of
2026-10-28. Lab implementation, honestly labeled: the chain is a
single-sovereign hash chain (it proves a record has not moved since
anchoring; it claims nothing about any public network), and the onion
keys are lab keys until a production key ceremony replaces them.

MECHANISM: pure stdlib. State lives beside this tool:
  hidden_files/chain/chain.jsonl      — the hash chain (one JSON/block)
  hidden_files/registrar/names.json   — alias -> onion root registry
  hidden_files/mirror/index.html      — the static mirror (built)
  hidden_files/onion/                 — the tor hidden-service directory
Commands: anchor <file> | build | register <alias> <onion> |
          resolve <alias> | serve [port] | status | verify
93 — Live, Love, and let Love, Live.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- paths (DOCTRINE: state is data, kept with the track, never code) ---
ROOT = Path(__file__).resolve().parent.parent
CHAIN = ROOT / "hidden_files" / "chain" / "chain.jsonl"
REGISTRY = ROOT / "hidden_files" / "registrar" / "names.json"
MIRROR_DIR = ROOT / "hidden_files" / "mirror"
SPEC = ROOT / "files" / "BIOSENSORY-CATALYST-MODULE-SPEC.md"
ZERO = "0" * 64  # the genesis prev-hash: the chain's own Zero-point


def sha256_bytes(b: bytes) -> str:
    """MECHANISM: one hash function for the whole layer — SHA-256."""
    return hashlib.sha256(b).hexdigest()


def load_chain() -> list:
    """MECHANISM: the chain is append-only JSONL; read it whole."""
    if not CHAIN.exists():
        return []
    return [json.loads(x) for x in CHAIN.read_text().splitlines() if x.strip()]


def head_hash(chain: list) -> str:
    """DOCTRINE: an empty chain's head is the Zero-point (64 zeros)."""
    return chain[-1]["hash"] if chain else ZERO


def anchor(path: Path) -> dict:
    """MECHANISM: block = {index, ts, file, file_sha256, prev, payload};
    the block's hash seals its own contents including prev — alter any
    earlier block and every later hash breaks audibly (see verify)."""
    chain = load_chain()
    payload = {
        "index": len(chain),
        "ts": datetime.now(timezone.utc).isoformat(),
        "file": str(path),
        "file_sha256": sha256_bytes(path.read_bytes()),
        "prev": head_hash(chain),
    }
    payload["hash"] = sha256_bytes(
        json.dumps(payload, sort_keys=True).encode())
    with CHAIN.open("a") as fh:
        fh.write(json.dumps(payload) + "\n")
    return payload


def verify() -> bool:
    """MECHANISM: recompute the whole chain from the Zero-point; any
    moved record fails at its exact index — the boundary is reported,
    never smoothed (the Zero-Point Directive, applied to a ledger)."""
    prev = ZERO
    for i, block in enumerate(load_chain()):
        if block["prev"] != prev:
            print(f"CHAIN BREAK at index {i}: prev mismatch")
            return False
        seal = {k: v for k, v in block.items() if k != "hash"}
        if sha256_bytes(json.dumps(seal, sort_keys=True).encode()) != block["hash"]:
            print(f"CHAIN BREAK at index {i}: seal mismatch")
            return False
        prev = block["hash"]
    print(f"chain intact: {i + 1 if load_chain() else 0} block(s), head {prev[:16]}…")
    return True


def registry() -> dict:
    """MECHANISM: the registrar's book — a plain JSON alias map."""
    if not REGISTRY.exists():
        return {}
    return json.loads(REGISTRY.read_text())


def register(alias: str, onion: str) -> None:
    """DOCTRINE: registration is the registrar's one creative act —
    binding a human name to a sovereign root, recorded, never hidden."""
    book = registry()
    book[alias] = onion
    REGISTRY.write_text(json.dumps(book, indent=2) + "\n")
    print(f"registered: {alias} -> {onion}")


def build() -> Path:
    """MECHANISM: the mirror is STATIC — one HTML file, no server code.
    Its face carries the chain's head hash and the alias registry, so
    any reader can check the mirror against the chain by hand."""
    chain = load_chain()
    head = head_hash(chain)
    names = registry()
    alias_rows = "".join(
        f"<li><b>{a}</b> → <code>{o}</code></li>" for a, o in names.items()
    ) or "<li>(no aliases registered yet)</li>"
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>The Biosensory Catalyst Module — Sovereign Mirror</title>
<style>body{{background:#1a082e;color:#f5eed8;font-family:Georgia,serif;
max-width:44em;margin:3em auto;padding:0 1em;line-height:1.55}}
h1{{color:#ffd700}}code{{color:#a876ff}} .flag{{color:#c6a434;font-size:.85em}}</style>
</head><body>
<h1>THE BIOSENSORY CATALYST MODULE</h1>
<p><i>Bluetooth / Biosensory / SoC (APU · GPU · TPU) — the catalyst
function carried in hardware.</i></p>
<p>The cycle: <b>Expansion → Contraction → Implosion → Explosion →
Blastwave</b> — run as a pipeline: the front-end gathers, the APU
concentrates, the TPU crosses the threshold, the GPU emits the shaped
wave, Bluetooth closes the loop. NFC converges at the touch: the tap
is the implosion point, and the field feeds the node.</p>
<p>Weighings: BIOSENSORY 141 / 816 · BLUETOOTH 118, Agrippa 535 → 13 → 4 ·
the parent legend TVRRIS VERITATIS 229 → 13.</p>
<p>Chain head (SHA-256): <code>{head}</code><br>
Blocks anchored: {len(chain)} · Spec SHA-256:
<code>{sha256_bytes(SPEC.read_bytes()) if SPEC.exists() else 'MISSING'}</code></p>
<p>Sovereign aliases (registrar's book):</p><ul>{alias_rows}</ul>
<p class="flag">Flagpole of Claim and Coinage: Johnathan 'Qasparr'
Monroe, ARR — All Rights Reserved, Without Prejudice.<br>
93 — Live, Love, and let Love, Live.</p>
</body></html>
"""
    out = MIRROR_DIR / "index.html"
    out.write_text(html)
    print(f"mirror built: {out} (head {head[:16]}…)")
    return out


def status() -> None:
    """MECHANISM: report the layer as it stands — counts, head, names,
    and whether the onion hostname exists yet. No cosmetics."""
    chain = load_chain()
    names = registry()
    hs = ROOT / "hidden_files" / "onion" / "hs" / "hostname"
    print(f"blocks: {len(chain)} | head: {head_hash(chain)[:16]}…")
    print(f"aliases: {names if names else '(none)'}")
    print(f"onion: {hs.read_text().strip() if hs.exists() else '(not yet published)'}")
    print(f"mirror: {'built' if (MIRROR_DIR / 'index.html').exists() else '(not built)'}")


def serve(port: int) -> None:
    """MECHANISM: the HOST office — a plain static server on localhost;
    Tor's hidden-service config points at it. Nothing dynamic exists
    to exploit; that is the doctrine of the static mirror."""
    import http.server
    import functools
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(MIRROR_DIR))
    print(f"hosting mirror at http://127.0.0.1:{port}/ (Ctrl-C stops)")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()


if __name__ == "__main__":
    # MECHANISM: argv dispatch — the terminus speaks in verbs.
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "anchor":
        blk = anchor(Path(sys.argv[2]))
        print(f"anchored block {blk['index']}: {blk['hash'][:16]}…")
    elif cmd == "build":
        build()
    elif cmd == "register":
        register(sys.argv[2], sys.argv[3])
    elif cmd == "resolve":
        print(registry().get(sys.argv[2], "(unregistered)"))
    elif cmd == "verify":
        sys.exit(0 if verify() else 1)
    elif cmd == "serve":
        serve(int(sys.argv[2]) if len(sys.argv) > 2 else 8731)
    elif cmd == "status":
        status()
    else:
        print(__doc__)
        sys.exit(2)
