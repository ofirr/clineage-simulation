import os
import yaml

from src import utils
from src import const


def get_git_hash(path_git_repository):

    cmds = [
        'git',
        '--git-dir', os.path.join(path_git_repository, '.git'),
        'show',
        '-s',
        '--format=%H'
    ]

    stdout, _, _ = utils.run_command(
        cmds,
        get_output=True
    )

    return stdout


def get_version_hclsim():

    return get_git_hash('.')


def get_version_clineage():

    return get_git_hash(
        "/home/{}/clineage/".format(os.environ['USER'])
    )


def get_version_estgt():

    return get_git_hash(
        const.PATH_ESTGT_GIT
    )


def get_version_treecmp():

    cmds = [
        'java',
        '-jar', const.PATH_TREECMP_BIN
    ]

    stdout, _, _ = utils.run_command(
        cmds,
        get_output=True
    )

    # 'TreeCmp version build2\n\nusage: java -jar TreeCmp.jar -s|-w <size>|-m|-r...
    version = stdout.splitlines()[0].split(' ')[2]

    return version


def write_python_packages_info(path_out):

    stdout, _, _ = utils.run_command(
        ['pip', 'freeze'],
        get_output=True
    )

    with open(path_out, 'wt') as stream:
        stream.write(stdout)
        stream.write('\n')


def write_conda_packages_info(path_out):

    stdout, _, _ = utils.run_command(
        ['conda', 'list'],
        get_output=True
    )

    with open(path_out, 'wt') as stream:
        stream.write(stdout)
        stream.write('\n')


def record_versions(path_out_base):

    versions = {}

    versions['HCLSIM'] = get_version_hclsim()
    versions['CLineage'] = get_version_clineage()
    versions['eSTGt'] = get_version_estgt()
    versions['treeCmp'] = get_version_treecmp()
    versions['TMC'] = '?'

    root = {
        'versions': versions
    }

    # write
    path_out_core = os.path.join(path_out_base, 'versions.core.yml')

    with open(path_out_core, 'wt') as stream:
        yaml.dump(root, stream, default_flow_style=False)

    # write output of pip freeze
    path_out_pip_freeze = os.path.join(path_out_base, 'versions.deps.pip')

    write_python_packages_info(path_out_pip_freeze)

    # write output of conda freeze
    path_out_conda_list = os.path.join(path_out_base, 'versions.deps.conda')

    write_conda_packages_info(path_out_conda_list)
