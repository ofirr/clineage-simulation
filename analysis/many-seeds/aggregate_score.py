import os
import glob
import json
import argparse
import re
import pandas as pd
import yaml
import sys
sys.path.append('../..')
from src import const


def get_triples_score(path_score):

    df_metrics = pd.read_csv(
        path_score,
        sep='\t',
        nrows=1
    )

    return df_metrics['Triples_toYuleAvg'][0]


def read_triples_score(path_scores_raw_out):

    score = get_triples_score(path_scores_raw_out)

    return score


def run(path_project, seed):

    path_genotyping_config = os.path.join(
        path_project, const.FILE_CONFIG_GENOTYPING
    )

    # read genotyping params
    params_list = None

    if os.path.exists(path_genotyping_config):
        with open(path_genotyping_config, 'rt') as stream:
            params_list = yaml.load(stream)

    config_jsons = []

    # read config.list
    with open(os.path.join(path_project, "config.list"), 'rt') as fin:
        names = fin.read().splitlines()
        # remove empty strings
        names = list(filter(None, names))
        # add to the final list
        config_jsons.extend(names)

    results = []

    for config_json_filename in config_jsons:

        with open(os.path.join(path_project, config_json_filename), 'rt') as file_in:
            cfg = json.loads(file_in.read())

        try:

            if params_list:

                for params in params_list['genotyping']:

                    path_score = os.path.join(
                        path_project, cfg["pathRelativeOutput"], "n-{:06d}".format(
                            params['n']), const.FILE_COMPARISON_METRICS_RAW
                    )

                    score = get_triples_score(path_score)

                    results.append(
                        (seed, config_json_filename, params['n'], score)
                    )

            else:

                path_score = os.path.join(
                    path_project, cfg["pathRelativeOutput"], "scores.raw.out"
                )

                score = get_triples_score(path_score)

                results.append(seed, config_json_filename, None, score)

        except Exception as e:
            print(e)
            pass

    for seed, config_json_file_name, n, score in results:
        print("{0}\t{1}\t{2}\t{3:3.4f}".format(
            seed, config_json_file_name, n, score)
        )


def parse_arguments():

    parser = argparse.ArgumentParser(description='run simulation')

    parser.add_argument(
        "--project",
        action="store",
        dest="path_project",
        required=True
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    projects = glob.glob('{}/seed-*'.format(params.path_project))

    for prj in projects:
        match = re.search(r'seed-(\d+)', prj)
        if not match:
            continue
        seed = match.group(1)
        run(prj, seed)
