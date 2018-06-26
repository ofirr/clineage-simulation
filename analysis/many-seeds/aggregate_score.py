import os
import glob
import json
import argparse
import re
import pandas as pd


def get_triples_score(path_score):

    df_metrics = pd.read_csv(
        path_score,
        sep='\t',
        nrows=1
    )

    return df_metrics['Triples_toYuleAvg'][0]


def run(path_project, seed):

    config_jsons = []

    with open(os.path.join(path_project, "config.list"), 'rt') as fin:
        names = fin.read().splitlines()
        # remove empty strings
        names = list(filter(None, names))
        # add to the final list
        config_jsons.extend(names)

    for config_json_filename in config_jsons:

        with open(os.path.join(path_project, config_json_filename), 'rt') as file_in:
            cfg = json.loads(file_in.read())

        try:
           path_score = os.path.join(path_project, cfg["pathRelativeOutput"], "scores.raw.out")
           score = get_triples_score(path_score)

           print("{0}\t{1}\t{2:3.4f}".format(seed, cfg["title"], score))
        except:
           pass


if __name__ == "__main__":

    projects = glob.glob('./seed-*')

    for prj in projects:
        match = re.search(r'seed-(\d+)', prj)
        if not match:
            continue
        seed = match.group(1)
        run(prj, seed)
        print()
