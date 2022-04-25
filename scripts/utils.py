#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" utils.py
    - utility functions for nf-exec

This file can also be imported as a module and contains the following functions:
    * vep_vcf_to_pandas

TO DO:  
    *
"""
from __future__ import absolute_import, division, print_function

# Python and 3rd party libraries 
import pandas as pd
from pathlib import Path

# Custom packages

__author__ = "Fernando Pozo"
__copyright__ = "Copyright 2022"
__license__ = "GNU General Public License"
__version__ = "1.0.1"
__maintainer__ = "Fernando Pozo"
__email__ = "fpozoc@gmx.com"
__status__ = "Development"

# Global variables

# Class declarations

# Function declarations
def vep_vcf_to_pandas(path:str, annotation:str, save:bool=True) -> pd.DataFrame():
    """
    Converts a VCF file with VEP annotations to a pandas dataframe.

    https://www.ensembl.org/info/docs/tools/vep/vep_formats.html

    Args:
        path (str): path to the VCF file
        annotation (str): name of the annotation to be extracted
        save (bool): whether to save the dataframe to a file
    
    Returns:
        pd.DataFrame: pandas dataframe with the annotation
    """
    consequences = "Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|DISTANCE|STRAND|FLAGS|VARIANT_CLASS|SYMBOL_SOURCE|HGNC_ID|CANONICAL|MANE|TSL|APPRIS|CCDS|ENSP|SWISSPROT|TREMBL|UNIPARC|GENE_PHENO|SIFT|PolyPhen|DOMAINS|miRNA|AF|AFR_AF|AMR_AF|EAS_AF|EUR_AF|SAS_AF|AA_AF|EA_AF|gnomAD_AF|gnomAD_AFR_AF|gnomAD_AMR_AF|gnomAD_ASJ_AF|gnomAD_EAS_AF|gnomAD_FIN_AF|gnomAD_NFE_AF|gnomAD_OTH_AF|gnomAD_SAS_AF|MAX_AF|MAX_AF_POPS|FREQS|CLIN_SIG|SOMATIC|PHENO|PUBMED|MOTIF_NAME|MOTIF_POS|HIGH_INF_POS|MOTIF_SCORE_CHANGE".split('|')

    df_vcf = pd.read_csv(path, sep='\t', comment='#', names=['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'sample_1'])
    df_csq = df_vcf['INFO'].str.split('CSQ=').str[1].str.split(',').explode().str.split('|', expand=True)
    df_csq.columns = consequences

    df = pd.merge(df_vcf.drop('INFO', axis=1), df_csq,  left_index=True, right_index=True)
    df['source'] = annotation
    if save:
        df.to_csv(Path(Path(path).parents[0], f'{annotation}.tsv.gz'), compression='gzip', sep='\t', index=None)
    return df