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

    score = get_triples_score(
        os.path.join(path_project)
    )

    print("{0}\t{1}%".format(seed, score))


if __name__ == "__main__":

    projects = glob.glob('./seed-*')

    for prj in projects:
        match = re.search(r'seed-(\d+)', prj)
        if not match:
            continue
        seed = match.group(1)
        run(prj, seed)
        print()
