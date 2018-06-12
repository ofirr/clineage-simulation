import os
import subprocess
import json
import argparse

ENV_MATLAB_KEY = 'matlab'
CONFIG_PATH_RELATIVE_OUTPUT = 'pathRelativeOutput'

FILE_SIMULATION_NEWICK = 'simulation.newick'
FILE_RECONSTRUCTED_NEWICK = 'reconstructed.newick'

PATH_ESTGT = './eSTGt/eSTGt'
PATH_RECONSTRUCT_LIB = './src/reconstruction'


def read_json_config(path):

    with open(path, 'rt') as file_in:
        return json.loads(file_in.read())


def run_command(cmd):
    "run command"

    process = subprocess.Popen(cmd)

    process.wait()


def run_matlab_code(path_matlab, matlab_code):
    "run matlab script"

    cmd = [
        os.path.join(path_matlab, 'matlab'),
        '-nodisplay', '-nosplash', '-nodesktop',
        '-r', matlab_code
    ]

    run_command(cmd)


def get_simulation_output_path(path_project, config_filename):

    # read simulation configuration
    config = read_json_config(os.path.join(path_project, config_filename))

    path_simulation_output = os.path.join(
        path_project, config[CONFIG_PATH_RELATIVE_OUTPUT]
    )

    return path_simulation_output


def highlight_tree_differences_to_png(path_matlab, path_simulation_newick, path_reconstructed_newick):

    matlab_code = "addpath('{0}', '{1}'); highlight_differences2('{2}', '{3}'); exit;".format(
        PATH_ESTGT, PATH_RECONSTRUCT_LIB, path_simulation_newick, path_reconstructed_newick
    )

    run_matlab_code(path_matlab, matlab_code)



def run(path_matlab, path_project, config_json):
    "run function"

    # get path to simulation output
    path_simulation_output = get_simulation_output_path(
        path_project, config_json
    )

    # highlight tree differences and save to png
    highlight_tree_differences_to_png(
        envs[ENV_MATLAB_KEY],
        os.path.join(path_simulation_output, FILE_SIMULATION_NEWICK),
        os.path.join(path_simulation_output, FILE_RECONSTRUCTED_NEWICK)
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

    # parse arguments
    params = parser.parse_args()

    # read environment configuration
    envs = read_json_config(params.path_env)

    if params.multi:
        with open(os.path.join(params.path_project, 'config.list'), 'rt') as fin:
            config_jsons = fin.read().splitlines()
    else:
        config_jsons = ['config.json']

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

        run(envs[ENV_MATLAB_KEY], params.path_project, config_json)
