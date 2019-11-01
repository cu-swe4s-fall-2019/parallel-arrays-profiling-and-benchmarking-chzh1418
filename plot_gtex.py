import data_viz
import gzip
import os
import argparse
import sys
import time
import importlib.util
import importlib
sys.path.append('hash-tables-chzh1418')
hash_functions = importlib.import_module('hash-tables-chzh1418.hash_functions')
hash_tables = importlib.import_module('hash-tables-chzh1418.hash_tables')

# Parse argument


def parse_args():
    parser = argparse.ArgumentParser(
            description='Pass parameters')
    parser.add_argument('--output_file',
                        type=str,
                        help='Output file name',
                        required=True)
    parser.add_argument('--group_type',
                        type=str,
                        help='Tissue group or type',
                        required=True)
    parser.add_argument('--gene_name',
                        type=str,
                        help='Gene name for plot',
                        required=True)
    parser.add_argument('--gene_reads',
                        type=str,
                        help='Gene counts data file',
                        required=True)
    parser.add_argument('--sample_attributes',
                        type=str,
                        help='Sample attributes and info',
                        required=True)
    return parser.parse_args()
# Define linear search function


def linear_search(key, L):
    """Function to search item in list

    Parameters
    --------
    key : item to search
    L : list for search

    Returns
    --------
    Index of matched items
    """
    hits = -1
    for i in range(len(L)):
        if L[i] == key:
            return i
            hits = 1
    return -1
    pass


def binary_search(key, D):
    lo = -1
    hi = len(D)
    while (hi - lo > 1):
        mid = (hi + lo) // 2

        if key == D[mid][0]:
            return D[mid][1]

        if (key < D[mid][0]):
            hi = mid
        else:
            lo = mid

    return -1


def sample_info_hash_table(group_col_name, sample_info_file_name):
    # get arguments for argparse
    # args = parse_args()
    sample_id_col_name = 'SAMPID'
    # Check file exist or not
    if (not os.path.exists(sample_info_file_name)):
        print('No sample info file')
        sys.exit(1)
    # Get all the samples and sample header info
    samples = []
    groups = []
    sample_info_header = None
    for line in open(sample_info_file_name):
        if sample_info_header is None:
            sample_info_header = line.rstrip().split('\t')
        else:
            samples.append(line.rstrip().split('\t'))
    # Search for group column index and sample id index
    group_col_idx = linear_search(group_col_name, sample_info_header)
    sample_id_col_idx = linear_search(sample_id_col_name, sample_info_header)
    if group_col_idx == -1:
        print('Tissue type not found')
        sys.exit(1)
    if sample_id_col_idx == -1:
        print('sample id not found')
        sys.exit(1)
    # Initiate hash table
    sample_info_hash = hash_tables.ChainedHash(
                       100000, hash_functions.h_rolling)
    for i in range(len(samples)):
        key = samples[i][group_col_idx]
        value = samples[i][sample_id_col_idx]
        search_result = sample_info_hash.search(key)
        if (search_result is None):
            # add in the hash table key value pairs
            sample_info_hash.add(key, [value])
            groups.append(key)
        else:
            search_result.append(value)
    return sample_info_hash, groups


def main():
    # get arguments from argparse
    t0 = time.time()
    args = parse_args()
    sample_info_file_name = args.sample_attributes
    group_col_name = args.group_type
    data_file_name = args.gene_reads
    gene_name = args.gene_name
    sample_id_col_name = 'SAMPID'
    # Check file exist or not
    if (not os.path.exists(data_file_name)):
        print('No data file input')
        sys.exit(1)
    # Call sample info hash table function
    sample_info_hash, groups = sample_info_hash_table(
                               group_col_name, sample_info_file_name)
    if len(groups) == 0:
        print('Could not find tissue type')
        sys.exit(1)
    version = None
    dim = None
    data_header = None
    group_counts = []
    # Get the data header and gene counts
    for l in gzip.open(data_file_name, 'rt'):

        if version is None:
            version = l
            continue

        if dim is None:
            dim = l
            continue

        if data_header is None:
            data_header = l.rstrip().split('\t')
            continue
        # Get all the gene counts
        gene_counts = l.rstrip().split('\t')

        if gene_counts[1] == gene_name:
            group_counts = []
            # Initiate the sample counts hash table
            sample_counts_hash = hash_tables.ChainedHash(
                                 100000, hash_functions.h_rolling)
            for group_idx in range(2, len(data_header)):
                # add in the sample counts hash table
                sample_counts_hash.add(data_header[group_idx],
                                       int(gene_counts[group_idx]))
            for i in range(len(groups)):
                counts = []
                sample_id = sample_info_hash.search(groups[i])
                if sample_id is None:
                    continue
                for j in sample_id:
                    sample_counts = sample_counts_hash.search(j)
                    if sample_counts is None:
                        continue
                    counts.append(sample_counts)
                group_counts.append(counts)
            t1 = time.time()
            print('hash table running time: ' + str(t1 - t0))
            data_viz.boxplot(group_counts, args.output_file, 'boxplot', groups)
            sys.exit(0)
    sys.exit(0)


if __name__ == '__main__':
    main()
