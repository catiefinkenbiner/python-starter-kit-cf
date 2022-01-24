from pathlib import Path
from subprocess import run


def main(*, python_exec: Path) -> None:
    """Pip installs project dependencies

    Args:
        python_exec: path to python executable

    Returns:

    """

    run([python_exec, "-m", "pip", "install", "--upgrade", "pip==20.0.2"])
    run([python_exec, "-m", "pip", "install", "--upgrade", "setuptools==45.1.0"])
    run([python_exec, "-m", "pip", "install", "-r", "requirements.txt"])
    run([python_exec, "-m", "pip", "install", "-r", "dev-requirements.txt"])
    print("Dependencies installed.")


def enforce_python_version() -> Path:
    """Returns the python executable if it meets version requirements

    Returns: path to python executable

    """
    import sys

    py_ver = sys.version_info
    fpy_ver = "{}.{}.{}".format(py_ver.major, py_ver.minor, py_ver.micro)
    if py_ver.major != 3:
        print(
            "Error: Requires Python 3.6+. Your version:{}. "
            "Try using 'python3' instead of 'python' in your command.".format(fpy_ver)
        )
        sys.exit(1)
    elif py_ver.minor < 6:
        print("Error: Requires Python 3.6+. Your version:", fpy_ver)
        sys.exit(1)
    return Path(sys.executable)


if __name__ == "__main__":
    py_exec = enforce_python_version()
    main(python_exec=py_exec)
