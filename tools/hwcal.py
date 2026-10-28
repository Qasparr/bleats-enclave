#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWCAL — repair & recalibration procedures for the sovereign enclave.
Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice). 2026 e.v.
Method of Science, Aim of Religion.

DOCTRINE: a procedure announces itself before it touches anything.
Every action here is either (a) a measurement that recommends, or
(b) a local, reversible recalibration inside the enclave's own
custody (chain re-verification, mirror re-strike, tor relaunch with
fresh proxy configuration). Nothing reaches outside the enclave;
nothing touches a user's physical device — device procedures print
their steps for the owner's own hands (advise-only law).
MECHANISM: subcommands: clock (measure offset vs the Tor consensus
need), chain (verify + re-anchor), mirror (re-strike + re-serve
check), tor (relaunch per the in-invocation rule), battery (print
the owner's-hand calibration procedure for Android devices).
93 — Live, Love, and let Love, Live.
"""
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()


def clock():
    """MECHANISM: compare the local clock against an HTTPS Date header
    fetched through the proxy — the offset Tor will suffer, measured."""
    import urllib.request
    try:
        req = urllib.request.Request("https://example.org", method="HEAD")
        with urllib.request.urlopen(req, timeout=15) as resp:
            date = resp.headers.get("Date")
        from email.utils import parsedate_to_datetime
        remote = parsedate_to_datetime(date).timestamp()
        offset = time.time() - remote
        verdict = "within tolerance" if abs(offset) < 30 else \
            "DRIFTED — resync the host clock (timedatectl / ntp)"
        print(f"clock offset {offset:+.1f}s — {verdict}")
    except Exception as exc:  # DOCTRINE: name the failure plainly.
        print(f"clock check failed: {exc}")


def chain():
    """MECHANISM: delegate to CLITCOM — one chain-keeper, no forks."""
    tool = HERE.parent / "clitcom.py"
    if tool.exists():
        subprocess.run([sys.executable, str(tool), "verify"])
    else:
        print("clitcom not installed beside hwcal — chain unverified")


def mirror():
    """MECHANISM: re-strike the mirror from custody records via
    CLITCOM build; the onion serves the new bytes without restart."""
    tool = HERE.parent / "clitcom.py"
    if tool.exists():
        subprocess.run([sys.executable, str(tool), "build"])
    else:
        print("clitcom not installed beside hwcal — mirror not rebuilt")


def tor():
    """DOCTRINE: the in-invocation rule (MAGVS MAP §VIII.4) — the
    proxy credential rotates between shells, so tor's config must be
    generated and the daemon launched in ONE invocation. This
    procedure prints that rule and the launch shape; the operator
    runs it as one command so the credential is of that moment."""
    print("tor recalibration = relaunch under a fresh configuration:")
    print("  1. in ONE shell: regenerate torrc HTTPSProxy lines from "
          "$https_proxy")
    print("  2. in the SAME shell: launch tor -f <torrc> (expert bundle)")
    print("  3. confirm 'Bootstrapped 100%' before serving traffic")


def battery():
    """DOCTRINE: advise-only — the owner's hands, the owner's device.
    The Android battery recalibration, printed as steps."""
    print("Android battery recalibration (owner's hands):")
    print("  1. charge to 100% and hold 30 minutes on the charger")
    print("  2. use normally to near-empty (do not force deep drains)")
    print("  3. charge uninterrupted to 100% again")
    print("  4. if readings still swing, the gauge is software; if the")
    print("     cell swells or overheats, the cell is hardware — stop")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "clock"
    {"clock": clock, "chain": chain, "mirror": mirror,
     "tor": tor, "battery": battery}.get(cmd, clock)()
