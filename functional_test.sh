#!/bin/bash

test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_plot_gtex pycodestyle plot_gtex.py
assert_no_stdout

run test_data_viz pycodestyle data_viz.py
assert_no_stdout

run test_unittest pycodestyle unit_test_plot_gtex.py 
assert_no_stdout

run no_datafile python plot_gtex.py --gene_reads GTEX --sample_attributes TEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene_name FOXC1 --group_type SMTS --output_file test1.png 
assert_exit_code 1

run no_sample_info python plot_gtex.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEX --gene_name FOXC1 --group_type SMTS --output_file test2.png
assert_exit_code 1

run no_tissue_type python plot_gtex.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene_name FOXC1 --group_type AB --output_file test3.png
assert_exit_code 1

run test_filename_exit python plot_gtex.py --gene_reads GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene_name FOXC1 --group_type SMTS --output_file Foxc1.png
assert_exit_code 1
