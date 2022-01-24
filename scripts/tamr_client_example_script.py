"""This script demonstrates usage of the `tamr_client` package.

THIS SCRIPT DOES NOT REPRESENT BEST PRACTICES.
INSTEAD MIRRORING `example_script.py` AS CLOSELY AS POSSIBLE IS PRIORITIZED.
Because that script relies heavily on the `tamr_toolbox` which does not yet support `tamr_client`,
much of that functionality has been replaced with the functions `check` and `update_project`. Best
coding practices would suggest that these functions be defined elsewhere, i.e. as part of a custom
package. They are included in this script only for clarity, and should not be interpreted as a
recommendation of what should be included in a production script.
"""
from typing import Any, Callable, Iterator, List

import click
from os.path import join
from pathlib import Path
from pyrsistent import freeze

import tamr_client as tc
from tamr_toolbox import utils

from custom_package.example_subpackage import example_module

# Establish CONFIG and LOGGER as globals
# Use `freeze` to get an immutable object that cannot be modified
CONFIG = freeze(
    utils.config.from_yaml(
        join(Path(__file__).resolve().parents[1], "conf", "tamr_client_config.yaml")
    )
)
LOGGER = utils.logger.create("tamr_client_example_script", log_directory=CONFIG["logging_dir"])
# Let Tamr Toolbox itself also contribute to the log
utils.logger.enable_toolbox_logging(log_directory=CONFIG["logging_dir"])
# Configure the logs from imported packages
utils.logger.enable_package_logging("custom_package", log_directory=CONFIG["logging_dir"])


def run_end_to_end_workflow(
    session: tc.Session, instance: tc.Instance, *, project_ids: List[str], verbose: bool = False
) -> List[tc.Operation]:
    """Run multiple projects using tamr_client

    Args:
        session: An authenticated session
        instance: A Tamr instance
        project_ids: A list of projects to run
        verbose: Whether to log in detail

    Returns:
        All jobs run as part of the workflow
    """
    my_projects = [tc.project.by_resource_id(session, instance, id) for id in project_ids]
    if verbose:
        LOGGER.info(f"About to run projects: {[p.name for p in my_projects]}")

    return [op for project in my_projects for op in update_project(session, project)]


def operation_check(session: tc.Session, op: tc.Operation) -> tc.Operation:
    """Waits until a Tamr operation has resolved and raises an exception on failure

    This function extends the function tamr_client.operation.check to return the resolved operation

    Args:
        session: An authenticated session
        op: The Tamr operation to be checked

    Returns:
        The operation once it has resolved

    Raises:
        tc.operation.Failed: If the operation fails
    """
    tc.operation.check(session, op)
    return tc.operation.poll(session, op)  # Ensure the returned Operation is up to date


def update_project(session: tc.Session, project: tc.Project) -> Iterator[tc.Operation]:
    """Run all steps updating a project using tamr_client

    Args:
        session: An authenticated session
        project: A project to run

    Returns:
        All jobs run as part of the update

    Raises:
        tc.operation.Failed: If an operation fails during execution
    """
    ops: List[Callable[[tc.Session, Any], tc.Operation]]
    if isinstance(project, tc.MasteringProject):
        ops = [
            tc.mastering.update_unified_dataset,
            tc.mastering.generate_pairs,
            tc.mastering.update_pair_results,
            tc.mastering.update_cluster_results,
            tc.mastering.publish_clusters,
        ]
    elif isinstance(project, tc.CategorizationProject):
        ops = [tc.categorization.update_unified_dataset, tc.categorization.update_results]
    elif isinstance(project, tc.SchemaMappingProject):
        ops = [tc.schema_mapping.update_unified_dataset]
    elif isinstance(project, tc.GoldenRecordsProject):
        ops = [tc.golden_records.update, tc.golden_records.publish]
    else:
        raise TypeError(f"Project {project.name} is of an unsupported type {type(project)}.")
    for op in ops:
        yield operation_check(session, op(session, project))


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

    # Create a Tamr client session and instance
    session = tc.session.from_auth(tc.UsernamePasswordAuth(**CONFIG["my_instance_name"]["login"]))
    instance = tc.Instance(**CONFIG["my_instance_name"]["socket_address"])

    # Use a function from this script
    run_end_to_end_workflow(session, instance, project_ids=["1", "3"])

    if verbose:
        LOGGER.info("My script is done running.")


if __name__ == "__main__":
    main()
