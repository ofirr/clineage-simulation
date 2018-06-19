#!/usr/bin/env python
import math
import os
import subprocess
import argparse


def run_command(cmd):
    "run command"

    process = subprocess.Popen(cmd)

    process.wait()


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

    # power of 2 (n=3 to 14)
    loci_num_list = []
    for n in range(3, 14):
        loci = int(math.pow(2, n))
        loci_num_list.append( (n, loci) )

    # currently, the max num of loci (OM6 AC only)
    loci_num_list.append( (14, 9936) )

    for n, loci_num in loci_num_list:

        path_work = "seed-{0}/n-{1:03d}".format(seed, n)

        os.makedirs(path_work, exist_ok=True)

        run_command(
            ['unzip', 'tmc-template.zip', '-d', path_work]
        )

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
