#!/usr/bin/env python
import math
import os
import subprocess
import argparse


def run_command(cmd):
    "run command"

    process = subprocess.Popen(cmd)

    process.wait()


def main(seed):

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

    loci_num_list = []
    for i in range(1, 14):
        loci = int(math.pow(2, i))
        loci_num_list.append(loci)

    loci_num_list.append(9936)

    for i, loci_num in enumerate(loci_num_list):

        path_work = "tmc-{0}/n-{1:03d}".format(seed, i + 1)

        os.makedirs(path_work, exist_ok=True)

        run_command(
            ['unzip', 'tmc-template.zip', '-d', path_work]
        )

        with open(os.path.join(path_work, "simulation.xml"), 'wt') as fout:
            fout.write(xml.format(seed, loci_num))
            fout.write('\n')


def parse_arguments():

    # 431414
    # 910648
    # 181848
    # 263803
    # 145539
    # 136069
    # 869293
    # 579705
    # 549861
    # 875887

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

    main(params.seed)
