import sys
sys.path.append("/home/chun/clineage/")
import clineage.wsgi

import os
import yaml
import pandas as pd
import numpy as np
from scipy.io import loadmat
import random
from decimal import Decimal
import scipy.stats
import pickle

from src import const


def read_ado_consts_adam_795_ampli1_xL_coverage(
        path='/home/dcsoft/s/Ofir/matlab_795_ampli1_xL_coverage_abs_opt.mat'):
    # fixme: save .mat file differently - expose P and Q directly.
    x = loadmat(path)
    assert len(x['xL'][0]) == 290  #
    P = x['xL'][0][:90]
    Q = x['xL'][0][90:]
    return P, Q


class NoSuchCoverageCaseException(Exception):
    pass


def read_ado_consts(case='795_coverage'):
    if case == '795_coverage':
        return read_ado_consts_adam_795_ampli1_xL_coverage()
    raise NoSuchCoverageCaseException(case)


def sample(given_dist_sample, n):
    dist = scipy.stats.rv_histogram(np.histogram(given_dist_sample))
    return dist.rvs(size=n)


def generate_wga_proportion(df):

    # between 0.0 and 1.0
    df_out = pd.DataFrame(np.random.randint(0, 11, size=df.shape) / 10)
    df_out.index = df.index
    df_out.columns = df.columns

    return df_out


def add_wga_proportion(df, df_wga_proportion):

    # split by a single slash
    # take the only first two which are allele1 and allele2, ignoring the rest
    # join them back to return something like 15/16
    df_out = df.applymap(lambda x: '/'.join(x.split('/')[0:2]))

    # join wga proportion
    # e.g. 15/16/0.3
    df_out = df_out + '/' + df_wga_proportion.astype(str)

    return df_out


def generate_coverage(df, target_reads_per_sample, noise_constant, p, q):

    n1, n2 = df.shape
    consts1 = sample(q, n=n1)
    consts2 = sample(p, n=n2)

    # get coverage ratio by p times q
    coverage_df = pd.DataFrame(
        {i: [consts1[i] * consts2[j] for j in range(n2)]
         for i in range(n1)}).transpose()

    # get random noise from normal distribution
    random_df = pd.DataFrame(
        np.random.normal(loc=0, scale=noise_constant, size=df.shape))

    # add coverage ratio and noise
    randomized_coverage_df = coverage_df + random_df

    # ratio to actual coverage (num of reads)
    relative_total_reads = coverage_df.sum().sum()
    ado_const = n2 * target_reads_per_sample / relative_total_reads
    coverage_df_f = randomized_coverage_df * ado_const

    # negative num of reads to zero
    df_coverage = coverage_df_f.applymap(lambda x: max(int(x), 0))

    # set index and column
    df_coverage.index = df.index
    df_coverage.columns = df.columns

    return df_coverage


def signal_simulation(resd, a1, a2, a1_proportion, coverage, genotyping_confidence_threshold):

    coverage = min(
        int(5 * round(float(coverage) / 5)), max_resd_coverage
    )  # e.g. 95 is currect max reads coverage in simulated genotyping dict (resd)

    # return None if coverage is zero
    if not coverage:
        return None

    proportions = (round(Decimal(a1_proportion), 2),
                   Decimal('1.0') - round(Decimal(a1_proportion), 2))

    fk = ('AC', 30, min(a1, a2), abs(a2 - a1), proportions, coverage)
    # todo: no simulation value available
    if max([a1, a2]) >= 30:
        return None
    if fk not in resd:
        return None

    res = random.choice(resd[fk])

    if res['calling_score'] < genotyping_confidence_threshold:
        # convert frozenset to list
        # take each number in the list, convert to str
        # join them with '/'
        # e.g. 14/15
        return '/'.join([x for x in map(str, list(res['called_alleles']))])

    return None


def genotyping_simulation(data, confidence_threshold):

    allele1, allele2, proportion, coverage = data.split('/')

    return signal_simulation(
        resd,
        int(allele1), int(allele2), proportion, coverage,
        confidence_threshold
    )


def simulate_genotyping(df, confidence_threshold):
    "e.g. 17/15/0.5/529"

    df_out = df.applymap(
        lambda data: genotyping_simulation(data, confidence_threshold))

    return df_out


def get_simulation_by_cycles(ms_repeat_type):

    from sequencing.calling.models import SimulationsByCycles

    if ms_repeat_type == 'A':
        sbc = SimulationsByCycles.objects.get(
            name='A markov simulations',
        )
    elif ms_repeat_type == 'G':
        sbc = SimulationsByCycles.objects.get(
            name='G markov simulations',
        )
    elif ms_repeat_type == 'AC':
        sbc = SimulationsByCycles.objects.get(
            name='AC markov simulations',
        )
    else:
        raise Exception(
            "Unable to load simulation by cycles for " + ms_repeat_type)

    return sbc.get_simulations_dict()


def run_genotyping_simulation(path_project, path_simulation_output, seed):

    # set random seed
    random.seed(seed)
    np.random.seed(seed)

    path_genotyping_config = os.path.join(
        path_project, const.FILE_CONFIG_GENOTYPING
    )

    if not os.path.exists(path_genotyping_config):
        return

    with open(path_genotyping_config, 'rt') as stream:
        params_list = yaml.load(stream)

    p, q = read_ado_consts()

    # read mutation table
    df = pd.read_table(
        os.path.join(path_simulation_output, const.FILE_MUTATION_TABLE),
        index_col='names'
    )

    for case, params in enumerate(params_list["genotyping"]):

        print(case, params)

        # generate wga proportion (e.g. 0.5)
        df_wga_proportion = generate_wga_proportion(df)

        # ignore the previous wga proportion and add new proportion
        df2 = add_wga_proportion(df, df_wga_proportion)

        # generate coverage
        df_coverage = generate_coverage(
            df2,
            params['targetNumReadsPerSample'],
            params['noiseConstant'],
            p, q
        )

        # add coverage
        df_all = df2 + '/' + df_coverage.astype(str)

        df_final = simulate_genotyping(
            df_all,
            params.get('genotypingConfidenceThreshold')
        )

        # print(df_final.head())

        # create output directory
        path_genotype_simulation_output = os.path.join(
            path_simulation_output,
            "n-{0:06d}".format(params.get('n'))
        )
        os.makedirs(path_genotype_simulation_output, exist_ok=True)

        # write to file
        df_final.to_csv(
            os.path.join(
                path_genotype_simulation_output,
                'mutation_table.txt'
            ),
            sep='\t',
            na_rep='NaN'
        )


with open('/home/dcsoft/s/Ofir/calling_trials_ac_bi_prf_including_mono.pickle', 'rb') as f:
    resd = pickle.load(f)

df_resd = pd.DataFrame(
    list(resd.keys()),
    columns=['ms_type', 'amp_cycle', 'a1', 'delta', 'proportion', 'coverage']
)

max_resd_coverage = max(df_resd.coverage)
