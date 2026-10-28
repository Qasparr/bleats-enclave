# etc/ca — Axoneme Lab CA (LAB ONLY)

**LAB ONLY.** This is a private, self-signed lab certificate
authority. It is **not** publicly trusted, is **not** a public CA,
and must never be presented as one. It exists so the enclave's own
services (lab mail today; AVD nodes and internal services as they
come) can speak TLS to each other under a root the Founder controls.
Public trust is a separate, later gate (see STATUS.md, Production
Gates): it becomes possible only after domain registration, e.g.
Let's Encrypt via DNS-01 — and even then this lab CA remains the
enclave's **internal** CA permanently.

Filed 2026-10-28 under the Founder's CA-elevation approval
("elevate via self signed certificate", 13:09 EDT), as a follow-up
to the LAB BUILD order of the same day. Authorship attributed
exclusively to Johnathan 'Qasparr' Monroe (Greek, -ARR, All Rights
Reserved, Without Prejudice). 93 — Live, Love, and let Love, Live.

## Contents

| File | What it is | Custody |
|---|---|---|
| `ca.crt` | Axoneme Lab CA root certificate (public) | shareable inside the enclave |
| `ca.key` | CA private key | **chmod 600 — never leaves the lab, NEVER committed to git** |
| `mail.crt` / `mail.key` | Postfix server cert/key — SANs: mail.axone.me, mail.axoneme.education, axone.me, axoneme.education, localhost, 127.0.0.1 | key 600, never committed |
| `mail.chain.crt` | `mail.crt` + `ca.crt` concatenated — the file Postfix presents | public |
| `axone.me.crt` / `.key` | Server cert for the axone.me family — SANs incl. avd1–avd5.axone.me, localhost, 127.0.0.1 | key 600, never committed |
| `axoneme.education.crt` / `.key` | Server cert — SANs: axoneme.education, mail.axoneme.education, localhost, 127.0.0.1 | key 600, never committed |
| `*.ext` | The extension files the leaves were issued with (kept so issuance is reproducible and auditable) | public |
| `ca.srl` | CA serial counter | lab-local, not committed |

Validities: CA 3650 days; leaves 825 days. Fingerprints and
expiry dates of record live in STATUS.md §(a).5 — fingerprints and
subjects only; key material appears in no document, log, or repo.

## Rules

1. Private keys (`*.key`) are custody, not content: chmod 600,
   never copied into the git repo (the repo `.gitignore` enforces
   `etc/ca/*.key`), never printed, never logged.
2. Any enclave service that needs TLS gets a leaf from this CA —
   do not mint ad-hoc self-signed one-offs; one root, many leaves.
3. If the CA key is ever suspected compromised, the whole lab PKI
   is re-minted and STATUS.md records the new fingerprint with the
   old one marked superseded, never vanished.
