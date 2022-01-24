"""
This script creates a virtual environment.

This script will only run successfully when using python 3.6+
"""
from pathlib import Path
from install import enforce_python_version


def main(python_exec: Path, *, env_name="") -> None:
    """Creates a virtual environment

    Args:
        python_exec: path to python executable
        env_name: a name for the virtual environment

    Returns:

    """
    from subprocess import run
    import os

    env_name = env_name.strip()
    if env_name == "":
        dir_name = Path.cwd().name
        env_name = ".venv-" + dir_name

    print("Creating virtual environment named {} at in {}".format(env_name, os.getcwd()))
    run([python_exec, "-m", "venv", "./" + env_name])
    print("Virtual environment has been created at {}/{}".format(os.getcwd(), env_name))
    print("Run 'source {}/bin/activate' to enter the environment".format(env_name))


if __name__ == "__main__":
    import sys

    py_exec = enforce_python_version()

    if len(sys.argv) == 1:
        main(python_exec=py_exec)
    elif len(sys.argv) == 2:
        main(python_exec=py_exec, env_name=sys.argv[1])
    else:
        raise TypeError(
            "Too many arguments provided. Provide a name for your virtual environment "
            "or leave blank to use the default. "
            "Example command: 'python3 create-venv.py .my-venv-name' "
        )
