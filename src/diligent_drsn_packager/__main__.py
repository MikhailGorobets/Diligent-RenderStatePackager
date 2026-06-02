"""Forward all arguments to the bundled packager binary."""

import os
import subprocess
import sys

from . import get_executable_path


def main():
    exe = get_executable_path()
    args = [exe, *sys.argv[1:]]
    # os.execv doesn't preserve console/exit semantics on Windows; spawn-and-wait there.
    if sys.platform == "win32":
        return subprocess.run(args).returncode
    os.execv(exe, args)


if __name__ == "__main__":
    sys.exit(main())
