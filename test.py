import os
import subprocess

def run_command(cmd):

    process = subprocess.Popen(cmd)

    process.wait()


path_matlab='/usr/wisdom/matlabR2017a/bin'
path_matlab='/Applications/MATLAB_R2017b.app/bin'

path_eSTGt='~/projects/eSTGt/eSTGt'

path_config='/Users/dchun/projects/clineage-simulation/src/config.json'


cmd = [
    os.path.join(path_matlab, 'matlab'),
    '-nodisplay', '-nosplash', '-nodesktop',
    '-r', "addpath('{}'); cd('src'); run_simul('{}'); exit;".format(path_eSTGt, path_config)
]

run_command(cmd)
