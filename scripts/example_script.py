from tamr_toolbox import workflow
from tamr_toolbox import utils
import config_settings  # TODO: this won't work yet, because this file needs to be moved to the package.  See other PR.

# Read config, make Tamr Client, make logger
config = config_settings("../conf/config.yaml")
tamr = utils.client.create(**config["my_instance_name"])
LOGGER = utils.logger.create("my-script", log_directory=config["logging_dir"])

# Run multiple projects using tamr_toolbox
my_project_ids = ["1", "3", "7", "22"]
my_projects = [tamr.projects.by_resource_id(p_id) for p_id in my_project_ids]
LOGGER.info(f"About to run projects: {[p.name for p in my_projects]}")
workflow.jobs.run(my_projects)
