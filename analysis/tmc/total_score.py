import glob
import json
import argparse
import re


def run(seed):

    for sim_no in range(1, 15):

        list = glob.glob(
            "./seed-{0}/n-{1:03d}/*/diff-score.json".format(seed, sim_no)
        )

        global_total = 0
        global_same = 0

        for file in list:
            with open(file, 'rt') as fin:
                data = json.loads(fin.read())
                total = data['total']
                same = total - (data['diff'] + data['missing'])
                global_total += total
                global_same += same

        ratio = global_same / global_total
        print("{0}\ttmc-{1:03d}\t{2:1.3f}\t{3:2.1f}%".format(seed,
                                                             sim_no, ratio, ratio * 100.0))


def parse_arguments():

    parser = argparse.ArgumentParser(description='generate')

    parser.add_argument(
        "-s",
        "--seed",
        action="store",
        dest="seed",
        required=True,
        help="Either a single seed number or 'all' for all seeds (e.g. seed-123, seed-456, ...)"
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    if params.seed == 'all':
        projects = glob.glob('./seed-*')
        for prj in projects:
            match = re.search(r'seed-(\d+)', prj)
            if not match:
                continue
            seed = match.group(1)
            run(seed)
            print()

    else:
        run(params.seed)
