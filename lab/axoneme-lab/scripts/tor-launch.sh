#!/bin/bash
# =====================================================================
# tor-launch.sh — generate torrc + launch the LAB draft hidden service
#
#   93 — Live, Love, and let Love, Live.
#   Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
#   (Greek, -ARR, All Rights Reserved, Without Prejudice).
#   Filed 2026-10-28 under his LAB BUILD order (12:51 EDT).
#
# MECHANISM: this script exists because of a hard environment law —
# the egress proxy credential ROTATES between shell invocations, so
# the torrc (which must embed the current HTTPSProxy credential) has
# to be generated AND tor launched inside ONE invocation. Running
# this script is that one invocation. Do not split it.
#
# The hidden service is LAB grade: keys live in ../tor/hs-draft
# (chmod 700, never committed). HS port 80 forwards to the lab HTTP
# server on 127.0.0.1:8740. SOCKS for verification: 127.0.0.1:9050.
#
# DOCTRINE: described != delivered — publication is only claimed
# after two byte-identical fetches through Tor (see lab-verify).
# =====================================================================
set -eu
LAB="$HOME/workspace/lab/axoneme-lab"
TORBIN="$HOME/workspace/bin/tor-expert/tor/tor"
export LD_LIBRARY_PATH="$HOME/workspace/bin/tor-expert/tor"

# --- parse the CURRENT proxy credential from the environment ---------
RAW="${https_proxy:-${HTTPS_PROXY:-}}"
STRIPPED="${RAW#*://}"
CREDS="${STRIPPED%@*}"
HOSTPORT="${STRIPPED##*@}"
PUSER="${CREDS%%:*}"
PPASS="${CREDS#*:}"
PHOST="${HOSTPORT%%:*}"
PPORT="${HOSTPORT##*:}"

mkdir -p "$LAB/tor/data" "$LAB/tor/hs-draft" "$LAB/logs"
chmod 700 "$LAB/tor/data" "$LAB/tor/hs-draft"

cat > "$LAB/tor/torrc-draft" <<EOF
DataDirectory $LAB/tor/data
Log notice file $LAB/logs/tor-draft.log
SocksPort 127.0.0.1:9050
HiddenServiceDir $LAB/tor/hs-draft
HiddenServicePort 80 127.0.0.1:8740
HTTPSProxy $PHOST:$PPORT
HTTPSProxyAuthenticator $PUSER:$PPASS
EOF
chmod 600 "$LAB/tor/torrc-draft"

pkill -x tor 2>/dev/null || true
sleep 1
nohup "$TORBIN" -f "$LAB/tor/torrc-draft" </dev/null > "$LAB/logs/tor-stdout.log" 2>&1 &
echo "tor launched (pid $!) — torrc at $LAB/tor/torrc-draft"
