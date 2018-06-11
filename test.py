import os
import subprocess
import json
import argparse

def run_command(cmd):
    "run command"

    process = subprocess.Popen(cmd)

    process.wait()


def simulate(path_matlab):
    "run simulation"

    path_eSTGt='./eSTGt/eSTGt'
    path_simul_lib='./src/simulation'

    path_working='./examples/example-01'
    path_working='./analysis/tmc'

    # run MATLAB simulation
    matlab_code = "addpath('{0}', '{1}', '{2}'); run_simul('{2}', '{3}'); exit;".format(
        path_eSTGt, path_simul_lib, path_working, 'config-01.json'
    )

    cmd = [
        os.path.join(path_matlab, 'matlab'),
        '-nodisplay', '-nosplash', '-nodesktop',
        '-r', matlab_code
    ]

    run_command(cmd)

    import dendropy

    # read simulation.newick
    tree = dendropy.Tree.get_from_path(
        os.path.join(path_working, 'simulation.newick'),
        "newick"
    )

    # write ascii plot for simulation tree
    with open(os.path.join(path_working, 'simulation.ascii_plot.txt'), 'wt') as fout:
        fout.write(tree.as_ascii_plot())
        fout.write('\n')


def main():
    "main function"

    parser = argparse.ArgumentParser(description='run simulation')

    parser.add_argument(
        "--env",
        action="store",
        dest="path_config_env",
        required=True
    )

    params = parser.parse_args()

    with open(params.path_config_env, 'rt') as file_in:        
        envs = json.loads(file_in.read())

    simulate(envs['matlab'])


if __name__ == "__main__":

    main()
