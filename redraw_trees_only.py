import os
import subprocess
import json
import argparse

from src import const
from src import utils


def get_simulation_output_path(path_project, config_filename):

    # read simulation configuration
    config = utils.read_json_config(os.path.join(path_project, config_filename))

    path_simulation_output = os.path.join(
        path_project, config[const.CONFIG_PATH_RELATIVE_OUTPUT]
    )

    return path_simulation_output


def highlight_tree_differences_to_png(path_matlab, path_simulation_newick, path_reconstructed_newick):

    matlab_code = "addpath('{0}', '{1}'); highlight_differences2('{2}', '{3}'); exit;".format(
        const.PATH_ESTGT, const.PATH_RECONSTRUCT_LIB, path_simulation_newick, path_reconstructed_newick
    )

    utils.run_matlab_code(path_matlab, matlab_code)


def run(path_matlab, path_project, config_json):
    "run function"

    # get path to simulation output
    path_simulation_output = get_simulation_output_path(
        path_project, config_json
    )

    # highlight tree differences and save to png
    highlight_tree_differences_to_png(
        envs[const.ENV_MATLAB_KEY],
        os.path.join(path_simulation_output, const.FILE_SIMULATION_NEWICK),
        os.path.join(path_simulation_output, const.FILE_RECONSTRUCTED_NEWICK)
    )


def parse_arguments():

    parser = argparse.ArgumentParser(description='redraw trees only')

    parser.add_argument(
        "--env",
        action="store",
        dest="path_env",
        required=True
    )

    parser.add_argument(
        "--project",
        action="store",
        dest="path_project",
        required=True
    )

    parser.add_argument(
        "--config",
        nargs='+',
        dest="configs",
        required=True
    )

    # parse arguments
    params = parser.parse_args()

    # read environment configuration
    envs = utils.read_json_config(params.path_env)

    # get config json files
    config_jsons = utils.handle_config_args(
        params.path_project, params.configs
    )

    return params, envs, config_jsons


if __name__ == "__main__":

    params, envs, config_jsons = parse_arguments()

    for config_json in config_jsons:

        if not config_json:
            continue

        if not os.path.exists(os.path.join(params.path_project, config_json)):
            raise Exception("Unable to find {}".format(config_json))

        print()
        print("{} #############################################".format(config_json))
        print()

        run(envs[const.ENV_MATLAB_KEY], params.path_project, config_json)
