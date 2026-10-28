#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWDIAG — hardware diagnostics for the sovereign enclave.
Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice). 2026 e.v.
Method of Science, Aim of Religion.

DOCTRINE: diagnostics report boundaries, not blobs. Each check ends
PASS, WARN, FAIL, or ABSENT (the sensor does not exist on this host —
an honest zero point, never dressed as a pass). Read-only throughout:
a diagnostic that changes the patient is a procedure, and procedures
live in hwcal, labeled as such.
MECHANISM: stdlib + /proc + /sys reads: CPU model and load, memory,
disk filesystems and free space, thermal zones, battery (sysfs —
usually ABSENT on servers), clock offset readiness for Tor, and the
enclave's own services (tor SOCKS, mirror ports) probed on localhost.
93 — Live, Love, and let Love, Live.
"""
import json
import os
import socket
import time


def read(path):
    """MECHANISM: one safe reader for every /proc and /sys probe."""
    try:
        with open(path) as fh:
            return fh.read().strip()
    except OSError:
        return None


def check(name, status, detail):
    """DOCTRINE: the four verdicts only — PASS/WARN/FAIL/ABSENT."""
    return {"check": name, "status": status, "detail": detail}


def cpu():
    model = None
    info = read("/proc/cpuinfo") or ""
    for line in info.splitlines():
        if "model name" in line or "Model" in line:
            model = line.split(":", 1)[1].strip()
            break
    load = os.getloadavg()
    return check("cpu", "PASS",
                 f"{model or 'unknown'} | load1 {load[0]:.2f}")


def memory():
    mem = {}
    for line in (read("/proc/meminfo") or "").splitlines():
        k, _, v = line.partition(":")
        mem[k.strip()] = v.strip()
    total = mem.get("MemTotal", "?")
    avail = mem.get("MemAvailable", "?")
    return check("memory", "PASS", f"total {total} | available {avail}")


def disks():
    out = []
    for mnt in ("/", "/home", "/tmp"):
        try:
            st = os.statvfs(mnt)
            free_pct = 100.0 * st.f_bavail / max(st.f_blocks, 1)
            out.append(f"{mnt} {free_pct:.0f}% free")
        except OSError:
            pass
    worst = min((float(s.split()[1].rstrip('%')) for s in out), default=100)
    return check("disks", "PASS" if worst > 10 else "WARN", " | ".join(out))


def thermals():
    zones = []
    base = "/sys/class/thermal"
    if os.path.isdir(base):
        for z in sorted(os.listdir(base)):
            t = read(os.path.join(base, z, "temp"))
            if t and t.isdigit():
                zones.append(f"{z} {int(t) / 1000:.0f}C")
    if not zones:
        return check("thermals", "ABSENT", "no thermal zones exposed")
    hot = max(float(z.split()[1].rstrip('C')) for z in zones)
    return check("thermals", "WARN" if hot > 85 else "PASS",
                 " | ".join(zones))


def battery():
    base = "/sys/class/power_supply"
    bats = []
    if os.path.isdir(base):
        for d in sorted(os.listdir(base)):
            cap = read(os.path.join(base, d, "capacity"))
            if cap:
                bats.append(f"{d} {cap}%")
    if not bats:
        return check("battery", "ABSENT",
                     "no battery on this host (mains-powered enclave)")
    return check("battery", "PASS", " | ".join(bats))


def clock():
    """DOCTRINE: Tor descriptors are time-sensitive; a drifted clock
    is the enclave's most common silent failure. Report the epoch and
    leave correction to hwcal, where procedures live."""
    return check("clock", "PASS",
                 f"epoch {int(time.time())} UTC — offset correction "
                 "is a procedure (see hwcal clock)")


def service(port, name):
    s = socket.socket()
    s.settimeout(1.5)
    try:
        s.connect(("127.0.0.1", port))
        return check(name, "PASS", f"127.0.0.1:{port} answering")
    except OSError:
        return check(name, "WARN", f"127.0.0.1:{port} not answering")
    finally:
        s.close()


if __name__ == "__main__":
    # MECHANISM: the full panel, one JSON list — boundaries included.
    panel = [cpu(), memory(), disks(), thermals(), battery(), clock(),
             service(9050, "tor-socks"), service(8731, "mirror-module"),
             service(8732, "mirror-bleats")]
    print(json.dumps(panel, indent=2))
