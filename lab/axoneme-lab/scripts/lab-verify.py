#!/usr/bin/env python3
# =====================================================================
# lab-verify.py — re-run the LAB verification battery end to end
#
#   93 — Live, Love, and let Love, Live.
#   Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
#   (Greek, -ARR, All Rights Reserved, Without Prejudice).
#   Filed 2026-10-28 under his LAB BUILD order (12:51 EDT).
#
# MECHANISM (stdlib only — a terminus that depends on nothing
# cannot be de-platformed by a package index):
#   1. DNS: dig @127.0.0.1 +tcp for A/MX/SOA of both lab zones and
#      the five AVD node names; assert the expected lab answers.
#      (TCP because the sandbox filters UDP replies on loopback —
#      observed 2026-10-28, dnsmasq logs "failed to send packet:
#      Operation not permitted" for UDP while TCP answers cleanly.)
#   2. MAIL: resolve the recipient zone's MX through the lab DNS,
#      speak SMTP to the resolved host, send a fresh token message
#      root@axone.me -> root@axoneme.education, then find the token
#      in the recipient Maildir spool and print its headers.
#   3. TOR: fetch the draft page through the local Tor SOCKS port
#      TWICE and compare sha256 of both fetches against the source
#      file on disk. Byte-identical or it did not happen.
#
# DOCTRINE: described != delivered. Every line below is a check
# against a live daemon or a file on disk — no claim is printed
# that the battery did not just perform.
# =====================================================================
import hashlib
import pathlib
import smtplib
import subprocess
import sys
import time

LAB = pathlib.Path.home() / "workspace/lab/axoneme-lab"
SPOOL = pathlib.Path("/var/lab-axoneme/mail-spool")
FAILURES = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")
    if not ok:
        FAILURES.append(name)


def dig(qname, qtype):
    out = subprocess.run(
        ["dig", "@127.0.0.1", qname, qtype, "+tcp", "+noall", "+answer"],
        capture_output=True, text=True, timeout=20).stdout.strip()
    return out


def expect(name, qname, qtype, needle):
    out = dig(qname, qtype)
    check(f"DNS {name}", needle in out, f"({qname} {qtype} -> ...{needle})")


# --- 1. DNS ------------------------------------------------------------
expect("apex A axone.me", "axone.me", "A", "127.0.0.1")
expect("apex A axoneme.education", "axoneme.education", "A", "127.0.0.1")
expect("MX axone.me", "axone.me", "MX", "mail.axone.me")
expect("MX axoneme.education", "axoneme.education", "MX",
       "mail.axoneme.education")
for i in range(1, 6):
    expect(f"node avd{i}", f"avd{i}.axone.me", "A", f"127.0.1.{i}")
expect("SOA axone.me", "axone.me", "SOA", "ns1.axone.me")

# --- 2. MAIL -----------------------------------------------------------
token = f"LABVERIFY-{int(time.time())}"
mx_line = dig("axoneme.education", "MX")
mx_host = mx_line.split()[-1].rstrip(".") if mx_line else ""
mx_ip = dig(mx_host, "A").split()[-1] if mx_host else ""
msg = (f"From: root@axone.me\r\nTo: root@axoneme.education\r\n"
       f"Subject: lab-verify {token}\r\n\r\nToken: {token}\r\n")
try:
    with smtplib.SMTP(mx_ip, 25, timeout=15) as s:
        s.ehlo("mail.axone.me")
        s.sendmail("root@axone.me", ["root@axoneme.education"], msg)
    sent = True
except Exception as exc:  # report, never smooth
    sent = False
    print(f"  smtp error: {exc}")
check("MAIL smtp accept via lab MX", sent, f"(MX {mx_host} at {mx_ip})")

landed = None
for _ in range(10):
    time.sleep(1)
    for f in (SPOOL / "axoneme.education").rglob("*"):
        if f.is_file() and token in f.read_text(errors="replace"):
            landed = f
            break
    if landed:
        break
check("MAIL delivered to spool", landed is not None,
      f"({landed if landed else 'token not found in Maildir'})")

# --- 3. TOR ------------------------------------------------------------
onion_file = LAB / "tor/hs-draft/hostname"
if onion_file.exists():
    onion = onion_file.read_text().strip()
    src = (LAB / "site/index.html").read_bytes()
    src_hash = hashlib.sha256(src).hexdigest()
    hashes = []
    for n in (1, 2):
        # curl, not urllib: the stdlib has no SOCKS client, and the
        # desk does not fake one. curl --socks5-hostname resolves
        # the .onion at the proxy, which is the correct semantics.
        p = subprocess.run(
            ["curl", "-s", "--max-time", "120",
             "--socks5-hostname", "127.0.0.1:9050", f"http://{onion}/"],
            capture_output=True, timeout=150)
        if p.returncode == 0 and p.stdout:
            hashes.append(hashlib.sha256(p.stdout).hexdigest())
        else:
            print(f"  tor fetch {n} error: curl rc={p.returncode}")
            hashes.append("")
    check("TOR fetch x2 byte-identical to source",
          hashes == [src_hash, src_hash],
          f"(onion {onion}; sha256 {src_hash[:16]}...)")
else:
    check("TOR onion minted", False, "(no hostname file)")

print("\nRESULT:", "ALL PASS" if not FAILURES else f"FAILURES: {FAILURES}")
sys.exit(1 if FAILURES else 0)
