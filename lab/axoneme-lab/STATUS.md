# STATUS — AXONEME LAB BUILD (2026-10-28)

**Authorship attributed exclusively to Johnathan 'Qasparr' Monroe**
(Greek, -ARR, All Rights Reserved, Without Prejudice).
Flagpole of Claim and Coinage: Johnathan 'Qasparr' Monroe, ARR, All
Rights Reserved, Without Prejudice. Method of Science, Aim of
Religion. Built under his LAB BUILD order, 2026-10-28 12:51 EDT.

## SCOPE

Everything in this document is **LAB**. The domains `axone.me` and
`axoneme.education` are **NOT registered** — registration waits on
two inputs only the Founder can supply (see Production Gates). The
lab runs on one VM: DNS and mail on loopback, the draft site on a
Tor hidden service. Nothing below claims a public registration, a
public mailbox, or a launched product. Described ≠ delivered: every
LAB-VERIFIED line quotes a check that was actually run; raw output
lives in `verification/`.

## (a) LAB-VERIFIED

### 1. Lab DNS registry/host — dnsmasq, authoritative for both zones

Daemon: dnsmasq (apt-installed this build), config
`etc/dnsmasq-lab.conf`, bound to 127.0.0.1:53, `aa` flag set.
Verified with `dig @127.0.0.1 +tcp` (full output:
`verification/dig-results.txt`):

```
axone.me.            A    127.0.0.1
axoneme.education.   A    127.0.0.1
axone.me.            MX   10 mail.axone.me.
axoneme.education.   MX   10 mail.axoneme.education.
mail.axone.me.       A    127.0.0.1
mail.axoneme.education. A 127.0.0.1
avd1.axone.me.       A    127.0.1.1      (AVD 5-node lab network)
avd2.axone.me.       A    127.0.1.2
avd3.axone.me.       A    127.0.1.3
avd4.axone.me.       A    127.0.1.4
avd5.axone.me.       A    127.0.1.5
axone.me.            SOA  ns1.axone.me. root.axone.me. 2026102801 7200 3600 1209600 600
```

**Boundary (measured):** UDP replies on loopback are filtered by
the sandbox — dnsmasq logs `failed to send packet: Operation not
permitted` and UDP digs time out. The same daemon answers cleanly
over **TCP**, which is the transport all evidence uses. On any
normal host both transports serve; here, TCP is the working road.

### 2. Lab mail daemon — Postfix, root@ both domains, delivery proven

Daemon: dedicated Postfix instance (`etc/postfix/main.cf`),
listening only on 127.0.0.1:25, virtual Maildir spools per domain
under `/var/lab-axoneme/mail-spool/<domain>/root/`.

Proof run (transcript: `verification/mail-test.txt`): the sender
resolved the recipient's MX **through the lab DNS**
(`axoneme.education MX → mail.axoneme.education → 127.0.0.1`), spoke
SMTP to that host, and Postfix delivered to the spool:

- Forward: `root@axone.me → root@axoneme.education`, queue ID
  `5CCBE2E27`, log verdict `status=sent (delivered to maildir)`.
  Delivered file preserved at `verification/delivered-message.txt`;
  sha256 `f536157f391318b05169fdb6f5ffb6a46a90a56f9915ab9ea2ebc553f7609fe6`
  (spool copy and evidence copy hash-identical).
- Reverse: `root@axoneme.education → root@axone.me`, queue ID
  `B4F8A2E98`, delivered (`verification/delivered-message-reverse.txt`).

Both mailboxes exist and receive. This is loopback lab mail: it
proves the daemon, the MX wiring, and the spools — not public
deliverability.

### 3. Bleats DRAFT site — Tor hidden service, byte-verified

Page: `site/index.html` (purple `#4B0082` / gold `#FFD700`,
rim-legend goat seal, "Say It. Spray It. Own It." +
"VOX CAPRI, VOX POPVLI. NVLLA VOX TACEBITVR", DRAFT banner,
contacts `root@bleats.com` and `root@axone.me` both marked
forthcoming). Served by http.server on 127.0.0.1:8740 behind:

**Onion: `2pdd2iu7xrjewn5vtuj65vsyrq4c6dozk2y6fzdkptt7lyjz5bn2lnid.onion`**

Tor (expert bundle) bootstrapped 100% at 2026-10-28T17:04:01Z.
Two independent fetches through Tor returned HTTP 200 and are
**byte-identical** to the source file (`cmp` clean):

```
3ebf221cea5e4b77578f61a18bbadba9857ed8a0f94aeb2b67e77316274d5b0d  site/index.html
3ebf221cea5e4b77578f61a18bbadba9857ed8a0f94aeb2b67e77316274d5b0d  onion fetch 1
3ebf221cea5e4b77578f61a18bbadba9857ed8a0f94aeb2b67e77316274d5b0d  onion fetch 2
70e1708105c12f7e699b0ae4bfe466feee0992f3e19b921f31ce65d4ca734d87  seal asset (source == through Tor)
```

(`verification/onion-verify.sha256`.) The hidden-service keys are
LAB keys in the working lab's `tor/hs-draft/` (chmod 700) and are
**not** in this repo.

### 4. Consolidated re-run

`scripts/lab-verify.py` (stdlib only) re-ran the whole battery
after the build: **13/13 PASS** — 10 DNS checks, SMTP accept via
lab MX, spool delivery, Tor fetch ×2 byte-identical
(`verification/lab-verify-run.txt`). After the CA elevation
(§5 below) the battery grew six cert/TLS checks and re-ran
**19/19 PASS** — every original check still green.

### 5. Lab CA — Axoneme Lab CA (private root, self-signed elevation)

Raised 2026-10-28 under the Founder's approval ("elevate via self
signed certificate", 13:09 EDT). A private root CA for the
enclave, living at `etc/ca/` (README there carries the custody
rules). Keys are chmod 600 and are **never** committed to the repo
(the repo `.gitignore` enforces `etc/ca/*.key`); only certificates
— public by design — appear here and in git.

**Root of record:**

```
subject  CN = Axoneme Lab CA, O = Axoneme Lab,
         OU = "LAB ONLY - internal enclave CA, not publicly trusted"
valid    2026-10-28 -> 2036-10-25 (3650 days, RSA-4096, CA:TRUE)
SHA-256  18:D8:89:C4:26:4B:5D:8A:CD:A3:FD:CF:6A:25:BC:7A:
         E6:E4:B6:B2:80:94:22:AB:04:B8:DA:D2:EA:15:F1:1D
```

**Leaves of record** (825 days each, all expire 2029-01-30;
`openssl verify` against the root: OK ×3):

```
mail.crt               CN mail.axone.me
  SANs  mail.axone.me, mail.axoneme.education, axone.me,
        axoneme.education, localhost, 127.0.0.1
  SHA-256 F9:1A:13:7D:3A:BE:28:F4:F9:7B:CF:5D:B9:6F:B9:1C:
          43:92:DB:2F:C0:25:18:9E:1C:80:FA:87:6C:A7:60:5B
axone.me.crt           CN axone.me
  SANs  axone.me, mail.axone.me, avd1-avd5.axone.me,
        localhost, 127.0.0.1
  SHA-256 A7:43:52:48:57:69:0B:CA:C6:8A:BA:35:A3:C3:98:5A:
          5D:2D:4D:CB:B3:B1:B0:03:DE:1C:F7:4F:9B:1C:58:A3
axoneme.education.crt  CN axoneme.education
  SANs  axoneme.education, mail.axoneme.education,
        localhost, 127.0.0.1
  SHA-256 D7:97:38:EA:1F:64:AB:E1:4B:CF:DB:54:40:06:5F:12:
          B4:23:FD:69:81:C1:EB:A4:33:E6:CA:E1:E4:FB:8C:63
```

**TLS wiring, verified live:**

- The lab Postfix instance presents `mail.chain.crt` (leaf + CA)
  with opportunistic STARTTLS (`smtpd_tls_security_level = may`;
  outbound `smtp_tls` trusts the lab CA). Plaintext delivery is
  untouched — elevation without breaking the proven road.
- Handshake: `openssl s_client -starttls smtp` to 127.0.0.1:25
  with the lab CA as trust anchor → **TLSv1.3,
  TLS_AES_256_GCM_SHA384, Verification: OK, Verify return
  code: 0** (`verification/tls-handshake.txt`).
- Delivery re-test after wiring: `root@axone.me →
  root@axoneme.education`, queue ID `0CC8531CE`,
  `status=sent (delivered to maildir)`, spool and evidence copies
  sha256-identical (`68114ebd…`;
  `verification/mail-test-tls.txt`,
  `verification/delivered-message-tls.txt`). A second message in
  the battery was delivered **over STARTTLS** end to end.

### Failures encountered during the build (all diagnosed, none hidden)

1. **First two Tor fetches returned HTTP 000.** Tor was still
   bootstrapping through the throttled egress proxy (45–50% while
   the 90-second fetches timed out). After bootstrap reached 100%
   the same fetches returned 200, byte-identical, repeatedly. The
   seal-asset fetch succeeded even in the first round (HTTP 200).
2. **First delivery deferred** (`dsn=4.3.5, mail system
   configuration error`): Postfix's `virtual(8)` agent could not
   open the mailbox map under the home mount — non-root users
   cannot traverse `/home/hatch` on this VM. Fixed by keeping the
   map of record here and a runtime copy at
   `/var/lab-axoneme/etc/virtual_mailbox` (`lab-up.sh` refreshes
   it; `main.cf` points there).
3. **Second deferral, same symptom:** the runtime directory
   `/var/lab-axoneme/etc` itself lacked other-traverse
   (`drwxrwx---`). `chmod 755` closed it; delivery then succeeded.
4. **`/var/log` differs between shell invocations** on this host
   (the mail log existed in one view, absent in another). The lab
   instance therefore logs to its own file via `maillog_file`
   (in `main.cf`) instead of relying on syslog.

## (b) PRODUCTION GATES — what the lab does NOT give him yet

1. **Domain registration — `axone.me` + `axoneme.education`.**
   Both confirmed unregistered (RDAP 404, 2026-10-28). Blocked on
   two Founder-only inputs: a **payment route** (registrars require
   a card/PayPal-class instrument; CashApp is his only rail and
   does not clear registrars) and **registrant details** (a mailing
   address). On registration, the records in
   `etc/dnsmasq-lab.conf` are the template to publish.
2. **Public mail.** A domain is names only until DNS points at an
   always-on host: production `root@axone.me` /
   `root@axoneme.education` need a public always-on mail host,
   public MX (plus SPF/DKIM/DMARC and PTR hygiene), and port 25
   egress/ingress. The lab daemon is loopback-only by design.
3. **`bleats.com` / `root@bleats.com`.** Registered since 2004,
   parked on CASHPARKING nameservers, expires 2027-07-02 — a
   domainer's asset with a price gate. Acquisition requires the
   Founder's **explicit word** (standing rule) and funds; until
   then `root@bleats.com` cannot exist and is marked forthcoming
   everywhere it appears.
4. **`axoneme.org` recovery.** Held by another party (registered
   2025-06-02, parked, expires 2027-06-02); his priority of first
   holding is proven by his commit history, not by current control.
   The road is dispute and/or expiry watch — not registration.
   `axoneme.dev` was also taken by another party (2026-06-11).
5. **Production Tor presence.** The draft onion above uses LAB
   keys on a sandbox VM. A production launch needs the Phase-2 key
   ceremony and a persistent host, per the Sovereign Name Layer
   record.
6. **Public TLS trust.** The Axoneme Lab CA (§5) is trusted only
   inside the enclave — no public browser or mail peer will accept
   its certificates, and it must never be offered as public trust.
   Publicly trusted certificates (e.g. Let's Encrypt via the
   DNS-01 challenge, which needs no public web server) become
   possible **only after registration** puts real DNS under the
   Founder's control, on a production host. That changes nothing
   for the lab CA: it remains the enclave's **internal** CA
   permanently — public leaves for public faces, lab leaves for
   the enclave's own wiring, two roots for two roads.

## Running state at filing

dnsmasq, the lab Postfix instance, the site server, and Tor are
**up** on the lab VM. `scripts/lab-up.sh` raises the stack,
`scripts/lab-down.sh` lowers it, `scripts/lab-verify.py` re-proves
it. Runtime state: `/var/lab-axoneme/`. Working lab (configs of
record, keys, evidence): `~/workspace/lab/axoneme-lab/`.

93 — Live, Love, and let Love, Live.
