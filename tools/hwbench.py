#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWBENCH — hardware benchmark for the sovereign enclave.
Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
(Greek, -ARR, All Rights Reserved, Without Prejudice). 2026 e.v.
Method of Science, Aim of Religion.

DOCTRINE: a benchmark is a measurement, not an advertisement. Every
figure is produced on the host that runs it, at the moment it runs,
and reported with its method beside it. Numbers end arguments.
MECHANISM: pure stdlib — CPU (integer + float loops), memory
bandwidth (large bytearray copies), disk (timed write/read of a
scratch file, removed after), hash throughput (SHA-256, the chain's
own function), and a composite report. No network, no writes outside
the scratch file.
93 — Live, Love, and let Love, Live.
"""
import hashlib
import json
import os
import platform
import sys
import time


def cpu_bench(seconds: float = 1.0) -> dict:
    """MECHANISM: count integer ops inside a fixed wall-clock window;
    the count IS the score — method printed with the result."""
    n = 0
    x = 0
    end = time.perf_counter() + seconds
    while time.perf_counter() < end:
        for i in range(10000):
            x += i * i
        n += 10000
    return {"int_ops_per_s": n / seconds, "checksum": x % 1000003}


def mem_bench(size_mb: int = 128) -> dict:
    """MECHANISM: time a full copy of a large buffer; bandwidth =
    bytes moved / seconds. Two moves (write+read) counted honestly."""
    buf = bytearray(os.urandom(size_mb * 1024 * 1024))
    t0 = time.perf_counter()
    dup = bytes(buf)
    dt = time.perf_counter() - t0
    moved = len(buf) * 2
    return {"copy_GB_per_s": round(moved / dt / 1e9, 2), "size_MB": size_mb,
            "sample": dup[:4].hex()}


def disk_bench(path: str = "/tmp", size_mb: int = 64) -> dict:
    """MECHANISM: write then read a scratch file with fsync on write —
    the honest number includes the flush. Scratch is always removed."""
    f = os.path.join(path, "hwbench-scratch.bin")
    data = os.urandom(1024 * 1024)
    try:
        t0 = time.perf_counter()
        with open(f, "wb") as fh:
            for _ in range(size_mb):
                fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        tw = time.perf_counter() - t0
        t0 = time.perf_counter()
        with open(f, "rb") as fh:
            while fh.read(1024 * 1024):
                pass
        tr = time.perf_counter() - t0
        return {"write_MB_per_s": round(size_mb / tw, 1),
                "read_MB_per_s": round(size_mb / tr, 1)}
    finally:
        if os.path.exists(f):
            os.remove(f)


def hash_bench(size_mb: int = 64) -> dict:
    """MECHANISM: SHA-256 throughput — the enclave's anchor function
    measured on this host, because chain-keeping speed is a budget."""
    data = os.urandom(size_mb * 1024 * 1024)
    t0 = time.perf_counter()
    hashlib.sha256(data).hexdigest()
    dt = time.perf_counter() - t0
    return {"sha256_MB_per_s": round(size_mb / dt, 1)}


if __name__ == "__main__":
    # MECHANISM: run the bench battery and print one JSON report —
    # machine-readable on purpose: diagnostics consume it (hwdiag).
    report = {
        "host": platform.node(),
        "machine": platform.machine(),
        "python": sys.version.split()[0],
        "cpu": cpu_bench(),
        "memory": mem_bench(),
        "disk": disk_bench(),
        "hash": hash_bench(),
    }
    print(json.dumps(report, indent=2))
