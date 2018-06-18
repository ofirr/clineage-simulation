import glob
import json
import argparse

def main(seed):

    for sim_no in range(1, 15):

        list = glob.glob("./tmc-{0}/tmc-{1:03d}/*/diff-score.json".format(seed, sim_no))

        global_total = 0
        global_same = 0

        for file in list:
            with open(file, 'rt') as fin:
                data = json.loads(fin.read())
                total = data['total']
                same = total - (data['diff'] + data['missing'])
                global_total += total
                global_same += same

        print("tmc-{0:03d}: {1:2.1f}%".format(sim_no, global_same / global_total * 100.0))


def parse_arguments():

    parser = argparse.ArgumentParser(description='generate')

    parser.add_argument(
        "--seed",
        action="store",
        dest="seed",
        required=True
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    main(params.seed)

