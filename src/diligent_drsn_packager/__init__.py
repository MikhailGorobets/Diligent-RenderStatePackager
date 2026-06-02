"""Prebuilt Diligent RenderStatePackager (binary wheel)."""

import os
import sys

__all__ = ["get_executable_path", "__version__", "__diligentcore_sha__"]


def _read_diligentcore_sha():
    path = os.path.join(os.path.dirname(__file__), "diligentcore_sha.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip() or "unknown"
    except OSError:
        return "unknown"


def get_executable_path():
    name = "Diligent-RenderStatePackager" + (".exe" if sys.platform == "win32" else "")
    path = os.path.join(os.path.dirname(__file__), "bin", name)
    if not os.path.isfile(path):
        raise FileNotFoundError("Bundled RenderStatePackager binary not found at " + path)
    return path


try:
    from importlib.metadata import PackageNotFoundError, version as _pkg_version

    try:
        __version__ = _pkg_version("diligent-drsn-packager")
    except PackageNotFoundError:
        __version__ = "0.0.0+unknown"
except Exception:
    __version__ = "0.0.0+unknown"

# DiligentCore commit the binary was built from; consumers compare it against their own pin.
__diligentcore_sha__ = _read_diligentcore_sha()
