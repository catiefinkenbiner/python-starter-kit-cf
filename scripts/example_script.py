from typing import List

import click
from os.path import join
from pathlib import Path

from tamr_unify_client import Client
from tamr_toolbox import utils
from tamr_toolbox import workflow
from tamr_unify_client.operation import Operation

from custom_package.example_subpackage import example_module

# Establish CONFIG and LOGGER as globals
CONFIG = utils.config.from_yaml(join(Path(__file__).resolve().parents[1], "conf", "config.yaml"))
LOGGER = utils.logger.create("example_script", log_directory=CONFIG["logging_dir"])
# Let Tamr Toolbox itself also contribute to the log
utils.logger.enable_toolbox_logging(log_directory=CONFIG["logging_dir"])
# Configure the logs from imported packages
utils.logger.enable_package_logging("custom_package", log_directory=CONFIG["logging_dir"])


def run_end_to_end_workflow(
    tamr: Client, *, project_ids: List[str], verbose: bool = False
) -> List[Operation]:
    """Run multiple projects using tamr_toolbox

    Args:
        tamr: A Tamr client
        project_ids: A list of projects to run
        verbose: Whether to log in detail

    Returns: All jobs run as part of the workflow

    """
    my_projects = [tamr.projects.by_resource_id(p_id) for p_id in project_ids]
    if verbose:
        LOGGER.info(f"About to run projects: {[p.name for p in my_projects]}")
    return workflow.jobs.run(my_projects)


@click.command()
@click.option("--verbose", is_flag=True, help="If this flag is present, verbose mode is enabled")
def main(verbose: bool) -> None:
    """An example function demonstrating using functions from the tamr-toolbox and
    the custom-package

    Args:
        verbose: Whether to log in detail

    """

    # Use the logger for this script
    LOGGER.info("My script is ready to run.")

    # Use a function from my package
    example_module.hello("Tamr")

    # Create a Tamr client
    tamr = utils.client.create(**CONFIG["my_instance_name"])

    # Use a function from this script
    run_end_to_end_workflow(tamr, project_ids=["1", "3"])

    if verbose:
        LOGGER.info("My script is done running.")


if __name__ == "__main__":
    main()
