# RE-TOOLKIT — the enclave's reverse-engineering & debugging suite

Installed and verified on the enclave host, 2026-10-28. All free,
all open-source, all staged durably under the workspace (never the
system package manager — the enclave owns its tools).

| Tool | Version | State |
|---|---|---|
| jadx | 1.5.1 | VERIFIED (runs) |
| apktool | 2.10.0 | VERIFIED (runs) |
| Ghidra | 11.3.2 PUBLIC | STAGED (analyzeHeadless present; needs the JRE below) |
| Frida (frida-tools) | 17.24.3 | VERIFIED (runs) |
| Temurin JRE | 21.0.13 LTS | VERIFIED (java runs) |
| binutils (objdump/readelf) + strace | host | VERIFIED (present) |
| gdb | — | ABSENT on this host — marked, not hidden |
| radare2 | 5.9.8 | Source staged; build pending — marked, not hidden |
| WireGuard (userspace, wireguard-go) | go1.23.4 build | VERIFIED — wg0 UP, 10.93.0.1/24, port 51820 |

Reproduce: `~/workspace/bin/install-re-and-wg.sh` (downloads release
builds into ~/workspace/bin/re-toolkit, builds wireguard-go).
