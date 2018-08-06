#!/usr/bin/env python
import math
import os
import shutil
import subprocess
import argparse
import json
import random
import glob
import yaml
from lxml import etree


def run_command(cmd):
    "run command"

    process = subprocess.Popen(cmd)

    process.wait()


def read_simulation_xml(path_xml):

    parser = etree.XMLParser(remove_blank_text=False)
    xdoc = etree.parse(path_xml, parser=parser)

    return xdoc


def read_yaml_config(path_yaml):

    with open(path_yaml, 'r') as stream:
        return yaml.load(stream)


def run(path_template):

    # read config.yml
    yaml_cfg = read_yaml_config(
        os.path.join(path_template, 'config.yml')
    )

    # initialize sseds
    seeds = []

    # add if there are pre-selected seeds
    if 'list' in yaml_cfg['seeds']:
        seeds.extend(yaml_cfg['seeds']['list'])

    # add additional seeds (random sample)
    how_many_seeds_generate = yaml_cfg['seeds']['generate']
    if how_many_seeds_generate > 0:
        seeds.extend(
            random.sample(range(100000, 999999), how_many_seeds_generate)
        )

    seeds = list(set(seeds))

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
        "--template",
        action="store",
        dest="path_template",
        default="./template",
        required=False
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    run(params.path_template)
