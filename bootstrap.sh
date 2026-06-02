#!/usr/bin/env bash
# Init submodules, build the packager, and stage the binary + provenance for `python -m build`.
# Linux also needs X11/xcb dev headers (configure-time dependency of DiligentTools' NativeApp).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

BUILD_TYPE="${1:-Release}"
PKG_DIR="src/diligent_drsn_packager"

git submodule update --init --recursive
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE="${BUILD_TYPE}"
cmake --build build --config "${BUILD_TYPE}" --target Diligent-RenderStatePackager

BIN="$(find build \( -name 'Diligent-RenderStatePackager' -o -name 'Diligent-RenderStatePackager.exe' \) -type f | head -n1)"
[ -n "${BIN}" ] || { echo "ERROR: packager binary not found under build/" >&2; exit 1; }

mkdir -p "${PKG_DIR}/bin"
cp "${BIN}" "${PKG_DIR}/bin/"
git -C DiligentCore rev-parse HEAD > "${PKG_DIR}/diligentcore_sha.txt"
echo "Staged ${BIN} (DiligentCore $(cat "${PKG_DIR}/diligentcore_sha.txt"))"
