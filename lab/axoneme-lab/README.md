# AXONEME LAB — DNS registry, mail daemon, Bleats draft (LAB BUILD)

**Authorship attributed exclusively to Johnathan 'Qasparr' Monroe**
(Greek, -ARR, All Rights Reserved, Without Prejudice).
Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All
Rights Reserved, Without Prejudice. Right of claim hereby reserved
and coined under the authority of the Living Man.
Method of Science, Aim of Religion. — Built 2026-10-28 under his
LAB BUILD order (12:51 EDT).

## Scope — read this first

This is a **LAB**. The domains `axone.me` and `axoneme.education`
are **not registered** (registration is gated on the Founder's
payment route and registrant details). Everything here runs on one
VM's loopback and a Tor hidden service, and is labeled LAB in every
file. `STATUS.md` separates what is **LAB-VERIFIED** (with the raw
verification output in `verification/`) from the **PRODUCTION
GATES** that remain. Described ≠ delivered: if a check is not in
`verification/`, this tree does not claim it.

## Layout

| Path | Office |
|---|---|
| `etc/dnsmasq-lab.conf` | Lab authoritative DNS for both zones: apex A, `www`, `mail`, `ns1`, MX, TXT, and the AVD 5-node names `avd1`–`avd5.axone.me` → 127.0.1.1–127.0.1.5. |
| `etc/postfix/` | Lab Postfix instance config (`main.cf`, stock `master.cf`, `virtual_mailbox` map): virtual mailboxes `root@axone.me` and `root@axoneme.education`, per-domain Maildir spools. |
| `site/` | Bleats DRAFT landing page (purple `#4B0082` / gold `#FFD700`, rim-legend seal, both motto registers, contacts marked forthcoming) + seal asset. |
| `scripts/lab-up.sh` | Raise the stack: dnsmasq, Postfix, HTTP server, Tor. |
| `scripts/tor-launch.sh` | Generate torrc **and** launch Tor in one invocation (environment law: the egress proxy credential rotates between shells). |
| `scripts/lab-verify.py` | Stdlib-only battery: dig checks, MX-routed SMTP delivery into the spool, two Tor fetches compared by sha256 against the source file. |
| `scripts/lab-down.sh` | Lower the stack (spools, keys, configs kept). |
| `verification/` | The evidence: dig output, SMTP transcripts, delivered messages with headers, hash files. |

## Runtime state (not in git)

Daemons keep state under `/var/lab-axoneme/` (queue, spools, logs):
the workspace mount will not let the delivery agent own files, and
Postfix's `virtual(8)` cannot traverse the home mount — so the
mailbox map is copied to `/var/lab-axoneme/etc/` at startup
(`lab-up.sh` does this) and `main.cf` points there. Tor keys live
in the working lab's `tor/hs-draft/` (chmod 700) and are **never
committed** — custody, not content. `.gitignore` enforces this.

## Known environment boundaries (measured, not assumed)

- **UDP DNS replies are filtered on loopback** by the sandbox
  (dnsmasq logs `failed to send packet: Operation not permitted`).
  The lab DNS answers over **TCP**; all dig evidence uses `+tcp`.
- Public inbound ports are unreachable on this VM; the Tor hidden
  service is the publication route.
- Tor bootstrap through the egress proxy is slow (minutes for
  descriptors). First fetches can time out while it warms.

93 — Live, Love, and let Love, Live.
