import glob
import json

for sim_no in range(1, 15):

    list = glob.glob("./tmc-{0:03d}/*/diff-score.json".format(sim_no))

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
