#!/bin/bash
# lab-down.sh — lower the LAB stack cleanly. LAB scope only.
# 93 — Live, Love, and let Love, Live. (Monroe, ARR, 2026-10-28)
LAB="$HOME/workspace/lab/axoneme-lab"
postfix -c "$LAB/etc/postfix" stop 2>/dev/null || true
pkill -x tor 2>/dev/null || true
pkill -x dnsmasq 2>/dev/null || true
pkill -f "http.server 8740" 2>/dev/null || true
echo "lab stack lowered (spools, keys and configs kept on disk)"
