import os

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

    stdout, stderr, errcode = utils.run_command(
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
        "./bin/eSTGt"
    )


def get_version_treecmp():

    cmds = [
        'java',
        '-jar', const.PATH_TREECMP_BIN
    ]

    stdout, stderr, errcode = utils.run_command(
        cmds,
        get_output=True
    )

    # 'TreeCmp version build2\n\nusage: java -jar TreeCmp.jar -s|-w <size>|-m|-r...
    version = stdout.splitlines()[0].split(' ')[2]

    return version


def record_versions():

    get_version_hclsim()
