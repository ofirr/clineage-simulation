#!/usr/bin/env python
import math
import os
import shutil
import subprocess
import argparse


def run(seed):

    xml = """
<Program>
<ExecParams>
    <SimTime>
        100
    </SimTime>
    <Seed>
        {0}
    </Seed>
</ExecParams>
<FunHandleName> update_rules </FunHandleName>
<Rule>
    <Prod>
        C -> 1 {{C,C}}_1
    </Prod>
    <InternalState>
        <Name> MS </Name>
        <InitVal> -1 </InitVal>
        <FuncHandleName> update_microsatellite </FuncHandleName>
        <DuplicateNum> {1} </DuplicateNum>
    </InternalState>
    <InternalState>
        <Name> Gen </Name>
        <InitVal> 0 </InitVal>
        <FuncHandleName> update_generation </FuncHandleName>
    </InternalState>
    <InitPop>
        1
    </InitPop>
</Rule>
</Program>
"""

    path_template = './template'

    # power of 2 (n=3 to 13)
    loci_num_list = []
    for n in range(3, 14): # inclusive and exclusive
        loci = int(math.pow(2, n))
        loci_num_list.append((n, loci))

    # currently, the max num of loci (OM6 AC only)
    # loci_num_list.append((14, 9936))

    for n, loci_num in loci_num_list:

        path_work = "seed-{0}/n-{1:03d}".format(seed, n)

        os.makedirs(path_work, exist_ok=True)

        # copy the template to new dir
        src_files = os.listdir(path_template)
        for file_name in src_files:
            full_file_name = os.path.join(path_template, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, path_work)

        with open(os.path.join(path_work, "simulation.xml"), 'wt') as fout:
            fout.write(xml.format(seed, loci_num))
            fout.write('\n')


def parse_arguments():

    parser = argparse.ArgumentParser(description='generate')

    parser.add_argument(
        "-s",
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

    run(params.seed)
