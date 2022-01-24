from tamr_toolbox import utils
from tamr_toolbox.models import data_type
from os.path import join
from os import mkdir
from pathlib import Path


def create_folder_if_does_not_exist(location):
    try:
        mkdir(location)
    except OSError:  # it's likely that the folder already exists
        pass


def config_settings(path_to_file: str) -> data_type.JsonDict:
    project_dir = Path(__file__).parents[1]
    my_config = utils.config.from_yaml("path_to_file")
    if not my_config.get('logging_dir'):
        my_config['logging_dir'] = join(project_dir, 'logs')
    if not my_config.get('data_input_root'):
        my_config['data_input_root'] = join(project_dir, 'data', 'sources')
    if not my_config.get('data_output_root'):
        my_config['data_output_root'] = join(project_dir, 'data', 'results')

    project_1_results_folder = join(my_config['data_output_root'], 'project_1_results')
    create_folder_if_does_not_exist(project_1_results_folder)

    return my_config
