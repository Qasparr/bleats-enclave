#!/bin/bash
# =====================================================================
# lab-up.sh — raise the whole LAB stack (DNS + mail + site + Tor)
#
#   93 — Live, Love, and let Love, Live.
#   Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
#   (Greek, -ARR, All Rights Reserved, Without Prejudice).
#   Filed 2026-10-28 under his LAB BUILD order (12:51 EDT).
#
# MECHANISM: four daemons, each started detached so it survives
# this shell: dnsmasq (lab DNS, 127.0.0.1:53), the lab Postfix
# instance (127.0.0.1:25), python http.server (draft site,
# 127.0.0.1:8740), and Tor via tor-launch.sh (its config MUST be
# generated in the same invocation that launches it — proxy
# credential rotation — so it stays a separate script).
#
# DOCTRINE: LAB scope only. The domains are unregistered; every
# service binds loopback; the only public surface is the Tor
# hidden service. Described != delivered: run lab-verify.py after.
# =====================================================================
set -u
LAB="$HOME/workspace/lab/axoneme-lab"
CFDIR="$LAB/etc/postfix"
RT=/var/lab-axoneme
mkdir -p "$RT/logs" "$RT/run" "$RT/etc"

echo "[1/4] DNS (dnsmasq, lab zones axone.me + axoneme.education)"
pgrep -x dnsmasq >/dev/null || \
  setsid nohup dnsmasq -C "$LAB/etc/dnsmasq-lab.conf" --no-daemon \
    </dev/null > "$RT/logs/dnsmasq-stdout.log" 2>&1 &

echo "[2/4] Mail (Postfix lab instance, virtual root@ both zones)"
# runtime copy of the mailbox map: the delivery agent cannot
# traverse the home mount, so the daemon reads the map from /var.
cp "$CFDIR/virtual_mailbox" "$RT/etc/virtual_mailbox"
postmap hash:"$RT/etc/virtual_mailbox"
chmod 755 "$RT/etc"; chmod 644 "$RT/etc/virtual_mailbox"*
postfix -c "$CFDIR" start 2>/dev/null || postfix -c "$CFDIR" reload

echo "[3/4] Draft site (http.server 127.0.0.1:8740)"
pgrep -f "http.server 8740" >/dev/null || \
  (cd "$LAB/site" && setsid nohup python3 -m http.server 8740 \
    --bind 127.0.0.1 </dev/null > "$RT/logs/http8740.log" 2>&1 &)

echo "[4/4] Tor hidden service (config + launch in one invocation)"
bash "$LAB/scripts/tor-launch.sh"

sleep 2
echo "--- lab stack raised; onion (if minted):"
cat "$LAB/tor/hs-draft/hostname" 2>/dev/null || echo "(tor still starting)"
