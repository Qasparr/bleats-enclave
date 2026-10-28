#!/bin/bash
# RE toolkit + wireguard-go installer — durable under ~/workspace/bin.
set -x
B=$HOME/workspace/bin
mkdir -p $B/re-toolkit $B/go-toolchain
cd $B/re-toolkit
# jadx (Android RE)
curl -sL -o jadx.zip https://github.com/skylot/jadx/releases/download/v1.5.1/jadx-1.5.1.zip && mkdir -p jadx && unzip -qo jadx.zip -d jadx && rm jadx.zip
# apktool
curl -sL -o apktool.jar https://github.com/iBotPeaches/Apktool/releases/download/v2.10.0/apktool_2.10.0.jar
# radare2
curl -sL -o r2.tar.gz https://github.com/radareorg/radare2/releases/download/5.9.8/radare2-5.9.8-w64.zip 2>/dev/null || true
curl -sL -o r2src.tar.gz https://github.com/radareorg/radare2/archive/refs/tags/5.9.8.tar.gz
# ghidra
curl -sL -o ghidra.zip https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.3.2_build/ghidra_11.3.2_PUBLIC_20250415.zip && unzip -qo ghidra.zip && rm ghidra.zip
# Go toolchain + wireguard-go
cd $B/go-toolchain
curl -sL -o go.tgz https://go.dev/dl/go1.23.4.linux-amd64.tar.gz && tar xzf go.tgz && rm go.tgz
export PATH=$B/go-toolchain/go/bin:$PATH GOPATH=$B/go-toolchain/gopath GOCACHE=$B/go-toolchain/gocache
go install golang.zx2c4.com/wireguard@latest 2>&1 | tail -2
ls $B/go-toolchain/gopath/bin/ 2>/dev/null
echo DONE-RE-WG
