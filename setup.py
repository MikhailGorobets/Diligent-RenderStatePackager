import os

from setuptools import find_packages, setup
from setuptools.dist import Distribution

try:
    from setuptools.command.bdist_wheel import bdist_wheel
except ImportError:
    from wheel.bdist_wheel import bdist_wheel


class BinaryDistribution(Distribution):
    # Force a platform-tagged (non-pure) wheel: it bundles a native binary, not Python code.
    def has_ext_modules(self):
        return True


class PlatformWheel(bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False

    def get_tag(self):
        # One ABI-agnostic wheel per platform; DRSP_WHEEL_PLAT lets CI set a manylinux tag.
        _python, _abi, plat = super().get_tag()
        return "py3", "none", os.environ.get("DRSP_WHEEL_PLAT", plat)


setup(
    distclass=BinaryDistribution,
    cmdclass={"bdist_wheel": PlatformWheel},
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={"diligent_drsn_packager": ["bin/*", "diligentcore_sha.txt"]},
    include_package_data=True,
)
