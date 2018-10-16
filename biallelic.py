from collections import Counter
import dendropy
import copy
import os
import pandas as pd

from src import const
import sys
sys.path.append("/home/{}/clineage/".format(const.WIS_USER))
import clineage.wsgi

from sequencing.calling.hist import Histogram as dHistogram
from sequencing.calling.simcor.hist_analysis import get_far_apart_highest_peaks, better_get_far_apart_highest_peaks,\
    better_get_far_apart_highest_peaks_that_doesnt_hang
from sequencing.calling.simcor.calling import get_peaks_ranges
from sequencing.calling.queries.order_this import binned_genotypes_bi
from sequencing.calling.queries.mutation_maps import transpose_dict


def special_get_population_kernels(
        genotypes, allele_number=2, minimal_distance_between_peaks=3, case=1,
        filter_ones=False, min_prop=0.2):

    if filter_ones:
        # Ignore single occurances
        h = dHistogram(
            {k: v for k, v in Counter(
                [a for ca in genotypes for a in ca]).items() if v > 1}
        )
        if len(h.keys()) == 0:
            return None
    else:
        h = dHistogram(Counter([a for ca in genotypes for a in ca]))

    if case == 1:
        return get_far_apart_highest_peaks(
            h,
            allele_number=allele_number,
            minimal_distance_between_peaks=minimal_distance_between_peaks,
            min_prop=min_prop)
    elif case == 2:
        return better_get_far_apart_highest_peaks(
            h,
            minimal_distance_between_peaks=minimal_distance_between_peaks,
            min_prop=min_prop)
    elif case == 3:
        return better_get_far_apart_highest_peaks_that_doesnt_hang(
            h,
            minimal_distance_between_peaks=minimal_distance_between_peaks)


def special_split_genotypes(cas, max_distance_from_peak=2, case=1, filter_ones=False, min_prop=0.2,
                            filter_single_peak=True, minimal_distance_between_peaks=3):

    peaks = special_get_population_kernels(
        [ca for i, ca in cas], allele_number=2, minimal_distance_between_peaks=minimal_distance_between_peaks, case=case,
        filter_ones=filter_ones, min_prop=min_prop)
    if peaks is None or len(peaks) > 2:
        return None
    if len(peaks) == 1 and filter_single_peak:
        return None
    peaks.sort()
    peaks_by_range = {p: prange for p, prange in zip(
        peaks, get_peaks_ranges(peaks, max_distance_from_peak))}
    calling_assignments = dict()
    for i, ca in cas:
        assigned_alleles = dict()
        for a in ca:
            for p in peaks_by_range:
                if a in peaks_by_range[p]:
                    assigned_alleles[a] = p
                    break
            else:
                pass  # TODO: allele was not assigned to a window, consider exception
        calling_assignments[(i, ca)] = assigned_alleles
    return calling_assignments


def get_bin_map_and_classifying_loci(ado_df, minimal_distance_between_peaks=2, filter_single_peak=False, ):

    bin_map = dict()
    peak_numbers_hemi = []
    no_peaks = []
    classifying_ms_by_grouping = dict()
    non_classifying_ms = list()
    for loc, data in ado_df.iterrows():
        #         print(loc)
        #         print(data.values)
        alleles_dropna = [(i, v)
                          for i, v in enumerate(data.values) if v is not None]
        if set(alleles_dropna) == set():
            continue
        #         print('after', alleles_dropna)
        calling_assignments = special_split_genotypes(alleles_dropna,
                                                      max_distance_from_peak=2,
                                                      minimal_distance_between_peaks=minimal_distance_between_peaks,
                                                      case=2,
                                                      filter_ones=False,
                                                      filter_single_peak=filter_single_peak, )
        if calling_assignments is None:
            continue
        ica = invert_calling_assignments(calling_assignments)
        bin_map[loc] = ica
        genotypes_iterable = binned_genotypes_bi(ica)
        for genotypes in genotypes_iterable:
            #         peaks = get_peaks(genotypes)
            top_classifying_alleles = tuple(
                sorted(Counter(genotypes).values(), reverse=True)[:2])
            if len(top_classifying_alleles) <= 1:
                non_classifying_ms.append(loc)
                continue
            classifying_ms_by_grouping.setdefault(
                top_classifying_alleles, list()).append(loc)
    return bin_map, classifying_ms_by_grouping, non_classifying_ms


def get_k_classifying_loci(classifying_ms_by_grouping, min_group_size=3):  # ?
    classifying_ms = list()
    for tca in classifying_ms_by_grouping:
        if min(tca) >= min_group_size:
            classifying_ms += classifying_ms_by_grouping[tca]
    return classifying_ms


def get_flat_mutation_table(ado_df, bin_map, classifying_ms):
    d = dict()
    for ms in bin_map.keys() & set(classifying_ms):
        for sr in bin_map[ms].keys():  # TODO: consider removing root
            sr_label = ado_df.columns[sr]
            for bin_key, allele in bin_map[ms][sr].items():
                binned_ms_key = '{}_{}'.format(ms, bin_key)
                if sr_label in d:
                    assert binned_ms_key not in d[sr_label]
                d.setdefault(sr_label, dict())[binned_ms_key] = int(allele)
    return d


def invert_calling_assignments(calling_assignments, average=False):

    ica = dict()
    for i, ca in calling_assignments:
        inverted_dict = dict()
        for allele, slot in calling_assignments[(i, ca)].items():
            inverted_dict.setdefault(slot, []).append(allele)
        if average:
            ica[i] = {k: sum(v) // len(v) for k, v in inverted_dict.items()}
        else:
            ica[i] = {k: v[0] for k, v in inverted_dict.items() if len(v) == 1}
    return ica


def convert(data):
    'convert a string e.g. 15/16 to a frozentset of 15, 16'

    # in case of allelic dropout
    if pd.isnull(data):
        return None

    # in mono case, pandas read it as float (e.g. 15.0)
    # convert to int and frozenset
    if type(data) == float:
        return frozenset({int(data)})

    alleles = list(map(int, data.split('/')))
    if len(alleles) == 2:
        return frozenset({alleles[0], alleles[1]})
    else:
        return frozenset({alleles[0]})


def method_A(path_mutation_table):

    df = pd.read_csv(
        path_mutation_table,
        sep='\t',
        index_col=0
    )

    df = df.applymap(convert)

    minimal_distance_between_peaks = 2
    filter_single_peak = False
    min_group_size = 3

    bin_map, classifying_ms_by_grouping, non_classifying_ms = get_bin_map_and_classifying_loci(
        df,
        minimal_distance_between_peaks=minimal_distance_between_peaks,
        filter_single_peak=filter_single_peak
    )

    classifying_ms = get_k_classifying_loci(
        classifying_ms_by_grouping,
        min_group_size=min_group_size
    )

    d = get_flat_mutation_table(df, bin_map, classifying_ms)

    calling = transpose_dict(copy.deepcopy(d))

    return calling


import sys
sys.path.append('/home/{}/s/Ofir/triplets/triplets/'.format(const.WIS_USER))
from TMC_CLI import parse_mutations_table, paired_triplets_generator, format_triplet
from triplets_input_generators.paired_triplets import parse_simulation_mut_table
from decimal import Decimal


def get_root_genotype(path_mutation_table):
    full_df = pd.read_table(path_mutation_table, index_col='names')
    full_df = full_df.applymap(lambda x: frozenset(x.split('/')[:2]))
    full_d = full_df.to_dict()
    return full_d['root']


def make_d(path_mutation_table, full_root_genotype):
    d = parse_simulation_mut_table(path_mutation_table)
    for loc in d:
        if len(full_root_genotype[loc]) == 1:
            prop = Decimal('1.0')
        elif len(full_root_genotype[loc]) == 2:
            prop = Decimal('0.5')
        else:
            raise ValueError(len(full_root_genotype[loc]))
        d[loc]['root'] = frozenset(
            {(int(v), prop) for v in full_root_genotype[loc]}
        )

    return d


def method_B(path_mutation_table):

    full_root_genotype = get_root_genotype(
        os.path.join(
            os.path.dirname(path_mutation_table),
            '..',
            path_mutation_table.split('/')[-1]
        )  # TODO: fix path
    )

    d = make_d(path_mutation_table, full_root_genotype)

    return d


class NoSuchMethod(Exception):
    pass


def get_method(name):

    if name == 'A':
        return method_A
    elif name == 'B':
        return method_B

    raise NoSuchMethod(name)
