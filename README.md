# Diligent RenderStatePackager

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/diligent-drsn-packager?logo=pypi&logoColor=white)](https://pypi.org/project/diligent-drsn-packager/)
[![Build](https://github.com/MikhailGorobets/Diligent-RenderStatePackager/actions/workflows/build.yml/badge.svg)](https://github.com/MikhailGorobets/Diligent-RenderStatePackager/actions/workflows/build.yml)

Prebuilt [Diligent Engine](https://github.com/DiligentGraphics/DiligentEngine) **RenderStatePackager**
command-line tool, distributed as a per-platform Python binary wheel on PyPI. It compiles declarative
render states (`.drsn` + HLSL) into a `DeviceObjectArchive` at build time, so an application can unpack
pipeline states at runtime through `IDearchiver` instead of compiling shaders on startup.

The wheel ships only the native executable — install it and run the tool, with no need to build the
packager (and all of DiligentCore + Dawn) from source.

| Platform | Wheel tag | Serialized backends |
| --- | --- | --- |
| Windows x64 | `win_amd64` | Direct3D11, Direct3D12, Vulkan, WebGPU |
| macOS arm64 | `macosx_11_0_arm64` | Vulkan, WebGPU |
| Linux x64 | `manylinux_2_28_x86_64` | Vulkan, WebGPU |

## Installation

```
pip install diligent-drsn-packager
diligent-drsn-packager --help
```

The wheel is independent of the Python ABI (`py3-none-<platform>`) and works with any Python 3.8+.

## Cloning the Repository

To build from source, clone with submodules:

```
git clone --recursive https://github.com/MikhailGorobets/Diligent-RenderStatePackager.git
```

If you cloned without `--recursive`, run `git submodule update --init --recursive`.

## Repository Structure

| Path | Description |
| --- | --- |
| `CMakeLists.txt` | Builds only the `Diligent-RenderStatePackager` executable |
| `src/diligent_drsn_packager/` | Python wrapper: `get_executable_path()` and a CLI passthrough |
| `pyproject.toml`, `setup.py` | Packaging into a platform-tagged binary wheel |
| `bootstrap.sh` | Init submodules, build, stage the binary |
| `.github/workflows/` | CI — build wheels (`build.yml`), publish to PyPI (`publish.yml`) |
| `DiligentCore`, `DiligentTools` | Pinned submodules |

## Build and Run Instructions

Requires CMake 3.19+, Ninja and a C++20 toolchain. On Linux also install X11/xcb development headers
(a configure-time dependency of DiligentTools' `NativeApp`): `apt install libx11-dev libxcb1-dev` or
`dnf install libX11-devel libxcb-devel`.

```
./bootstrap.sh            # init submodules, build, stage the binary
python -m build --wheel   # produce dist/*.whl
pip install dist/*.whl
```

## Usage from CMake

Resolve the executable from the installed wheel at configure time:

```cmake
find_package(Python3 COMPONENTS Interpreter REQUIRED)
set(_pfx "${CMAKE_BINARY_DIR}/_drsn_packager")
execute_process(COMMAND "${Python3_EXECUTABLE}" -m pip install --target "${_pfx}"
                "diligent-drsn-packager==0.1.0")
execute_process(
    COMMAND "${Python3_EXECUTABLE}" -c
            "import sys;sys.path.insert(0,r'${_pfx}');import diligent_drsn_packager as p;print(p.get_executable_path())"
    OUTPUT_VARIABLE PACKAGER_EXE OUTPUT_STRIP_TRAILING_WHITESPACE)
# e.g. ${PACKAGER_EXE} -o RenderStates.bin --vulkan --webgpu -s Shaders -r RenderStates -i Lib.drsn
```

## Version Compatibility

A `DeviceObjectArchive` is bound to DiligentCore's serialization format (header `ArchiveVersion`); an
archive only loads in a runtime built from a compatible DiligentCore commit. The wheel records the
commit it was built from in `diligent_drsn_packager.__diligentcore_sha__`. When the submodules are
bumped, release a new wheel version and pin to it in the consumer.

## Release

Set the version in `pyproject.toml`, then tag:

```
git tag v0.1.0 && git push --tags
```

`publish.yml` builds every platform wheel and uploads them to PyPI via Trusted Publishing (OIDC).
Configure the PyPI project's trusted publisher (this repository, environment `pypi`) beforehand.

## License

Apache-2.0 — see [LICENSE](LICENSE). Bundled binaries are built from DiligentCore and DiligentTools,
which are also licensed under Apache-2.0.
