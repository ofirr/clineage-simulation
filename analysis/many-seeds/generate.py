#!/usr/bin/env python
import math
import os
import shutil
import subprocess
import argparse
import json
import random
import glob
from lxml import etree


def run_command(cmd):
    "run command"

    process = subprocess.Popen(cmd)

    process.wait()


def read_simulation_xml(path_xml):

    parser = etree.XMLParser(remove_blank_text=False)
    xdoc = etree.parse(path_xml, parser=parser)

    return xdoc


def run(how_many_seeds):

    path_template = './template'

    # generate seeds
    seeds = random.sample(range(100000, 999999), how_many_seeds)
    #seeds = [140161,234776,254361,282174,479041,544815,605395,693355,712020,741576,741867,796476,912629,970154,397701,685610]
    
    # read the template simulation.xml
    xdoc = read_simulation_xml(
        os.path.join(path_template, 'simulation.xml')
    )

    # iterate through seeds
    for seed in seeds:

        print(seed)

        # create a seed directory
        path_work = "seed-{0}".format(seed)
        os.makedirs(path_work, exist_ok=True)

        # copy the template to new dir
        src_files = os.listdir(path_template)
        for file_name in src_files:
            full_file_name = os.path.join(path_template, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, path_work)

        # change seed
        xdoc.xpath('./ExecParams/Seed')[0].text = str(seed)

        # write the final xml to a file
        with open(os.path.join(path_work, 'simulation.xml'), 'wt') as fout:
            xml = etree.tostring(
                xdoc,
                method='xml',
                pretty_print=True,
                encoding="unicode"
            )
            # hack: eSTGt doesn't comply with the XML rules
            xml = xml.replace('&gt;', '>')
            fout.write(xml)

        # update the title key in config.json
        cfg_json_filenames = glob.glob(
            os.path.join(path_work, "*.json")
        )
        for cfg_json_file in cfg_json_filenames:
            with open(cfg_json_file, 'rt') as fin:
                cfg = json.loads(fin.read())
            cfg["title"] = "{} / Seed {}".format(cfg["title"], seed)
            with open(cfg_json_file, 'wt') as fout:
                fout.write(json.dumps(cfg, indent=4))


def parse_arguments():

    parser = argparse.ArgumentParser(description='generate')

    parser.add_argument(
        "--count",
        action="store",
        dest="how_many_seeds",
        required=True
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    run(
        int(params.how_many_seeds)
    )
