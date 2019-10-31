import data_viz
import gzip
import os
import argparse
import sys
import time
sys.path.append('hash-tables-chzh1418')
import hash_functions
import hash_tables
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


def main():
    # get arguments from argparse
    main_start = time.time()
    args = parse_args()
    data_file_name = args.gene_reads
    sample_info_file_name = args.sample_attributes
    group_col_name = args.group_type
    gene_name = args.gene_name
    sample_id_col_name = 'SAMPID'
    # Check file exist or not
    if (not os.path.exists(data_file_name)):
        print('No data file input')
        sys.exit(1)
    if (not os.path.exists(sample_info_file_name)):
        print('No sample info file')
        sys.exit(1)
    # Get all the samples and sample header info
    # Initiate hash table
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
    # group_col_idx = binary_search(group_col_name, sample_info_header)
    # sample_id_col_idx = binary_search(sample_id_col_name, sample_info_header)
    # members = []
    if group_col_idx == -1:
        print('Tissue type not found')
        sys.exit(1)
    if sample_id_col_idx == -1:
        print('sample id not found')
        sys.exit(1)
    sample_info_hash = hash_tables.ChainedHash(100000, hash_functions.h_rolling)    
    for i in range(len(samples)):
        key = samples[i][group_col_idx]
        value = samples[i][sample_id_col_idx]
        search_result = sample_info_hash.search(key)
        if (search_result is None):
            sample_info_hash.add(key, [value])
            groups.append(key)
        else:
            search_result.append(value)
    # print(sample_info_hash.search('Blood'))
    # return groups
    # print(groups)
        # sample_name = sample[sample_id_col_idx]
        # curr_group = sample[group_col_idx]
        # curr_group_idx = linear_search(curr_group, groups)
        # curr_group_idx = binary_search(curr_group, groups)
        # if curr_group_idx == -1:
        #    curr_group_idx == len(groups)
        #    groups.append(curr_group)
        #    members.append([])
        # members[curr_group_idx].append(sample_name)
    # Check if found tissue type
    if len(groups) == 0:
        print('Could not find tissue type')
        sys.exit(1)
    version = None
    dim = None
    data_header = None
    gene_name_col = 1
    # Column with gene name
    group_counts = []
    # Initiate another hash table
    sample_counts_hash = hash_tables.ChainedHash(100000, hash_functions.h_rolling)
    for l in gzip.open(data_file_name, 'rt'):
        if version is None:
            version = l
            continue
        if dim is None:
            dim = [int(x) for x in l.rstrip().split()]
            continue
        if data_header is None:
            # Sort data_header for binary search
            # Benchmarking for sorting
            # sort_start = time.time()
            data_header = l.rstrip().split('\t')
            continue
            # i = 0
            # for field in l.rstrip().split('\t'):
            #    data_header.append([field, i])
            #    i += 1
            #    data_header.sort(key=lambda tup: tup[0])
            #    continue
            # sort_end = time.time()
            # print('Sorting time: ' + str(sort_end - sort_start))

        # Searching benchmarking
        print(len(data_header))
        A = l.rstrip().split('\t')
        # add hash table
        if A[gene_name_col] == gene_name:
            # sample_counts_hash = hash_tables.ChainedHash(100000, hash_functions.h_rolling)
            group_counts = []
            for group_idx in range(2, len(data_header)):
                sample_counts_hash.add(data_header[group_idx], int(A[group_idx]))
        # hash table search
            for i in groups:
                counts = []
                sample_id = sample_info_hash.search(i)
                for j in sample_id:
                    sample_counts = sample_counts_hash.search(j)
                    counts.append(sample_counts)
                group_counts.append(counts)
        # print(sample_info_hash.search('Brain'))
        # print(sample_counts_hash.search('GTEX-ZZPU-0003-SM-5DWTO'))
        # if A[gene_name_col] == gene_name:
        #    search_start = time.time()
        #    for group_idx in range(len(groups)):
        #        for member in members[group_idx]:
                    # member_idx = linear_search(member, data_header)
        #            member_idx = binary_search(member, data_header)
        #            if member_idx != -1:
        #                group_counts[group_idx].append(int(A[member_idx]))
        #    search_end = time.time()
        #    print('Searching time : ' + str(search_end - search_start))
        data_viz.boxplot(group_counts, args.output_file, 'boxplot', groups)
    # main_end = time.time()
    # print('main prog running time: ' + str(main_end - main_start))
    sys.exit(0)


if __name__ == '__main__':
    main()
