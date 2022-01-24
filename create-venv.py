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
    environment_variable_lookup = {"TAMR_PROJECT_HOME": os.getcwd()}
    start_filename = "start.sh"
    with open(start_filename, "w") as f:
        f.write(f"#!/bin/bash\n")
        f.write(f'echo "Activating virtual environment {env_name}:"\n')
        command = f"source {env_name}/bin/activate"
        f.write(f'echo "{command}"\n')
        f.write(f"{command}\n")
        f.write('echo "Setting environment variables (edit start.sh to modify/add):"\n')
        for name in environment_variable_lookup:
            command = f'export {name}="{environment_variable_lookup[name]}"'
            f.write(f'echo "{command}"\n')
            f.write(f"{command}\n")

    print("Virtual environment has been created at {}/{}".format(os.getcwd(), env_name))
    print("Run 'source {}' to enter the environment".format(start_filename))


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
