import re
import os
import gzip
import string
import multiprocessing
import argparse
import logging

import pandas as pd

from utils import timeit, backup_file


logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s')


def parse_args():
    parser = argparse.ArgumentParser(
        description=('This script converts NCBI taxonomy (taxdump) into '
                     'lineages, save the information in csv.gz format'))

    parser.add_argument(
        '--nodes-file', required=True,
        help='NCBI taxonomy path/to/taxdump/nodes.dmp')

    parser.add_argument(
        '--names-file', required=True,
        help='NCBI taxonomy path/to/taxdump/names.dmp')

    parser.add_argument(
        '-o', '--output-prefix', default='ncbi_lineages',
        help='will output both lineage information in output_prefix.csv.gz')

    args = parser.parse_args()
    return args


@timeit
def load_nodes(nodes_file):
    '''
    load nodes.dmp and convert it into a pandas.DataFrame
    '''
    df = pd.read_csv(nodes_file, sep='|', header=None, index_col=False,
                     names=[
                         'tax_id',
                         'parent_tax_id',
                         'rank',
                         'embl_code',
                         'division_id',
                         'inherited_div_flag',
                         'genetic_code_id',
                         'inherited_GC__flag',
                         'mitochondrial_genetic_code_id',
                         'inherited_MGC_flag',
                         'GenBank_hidden_flag',
                         'hidden_subtree_root_flag',
                         'comments'
                     ])

    # To get rid of flanking tab characters
    df['rank'] = df['rank'].apply(string.strip)
    df['embl_code'] = df['embl_code'].apply(string.strip)
    df['comments'] = df['comments'].apply(string.strip)
    return df


@timeit
def load_names(names_file):
    '''
    load names.dmp and convert it into a pandas.DataFrame
    '''
    df = pd.read_csv(names_file, sep='|', header=None, index_col=False,
                     names=[
                         'tax_id',
                         'name_txt',
                         'unique_name',
                         'name_class'
                     ])
    df['name_txt'] = df['name_txt'].apply(string.strip)
    df['unique_name'] = df['unique_name'].apply(string.strip)
    df['name_class'] = df['name_class'].apply(string.strip)

    sci_df = df[df['name_class'] == 'scientific name']
    sci_df.reset_index(drop=True, inplace=True)
    return sci_df


def to_dict(lineage):
    """
    convert the lineage into a list of tuples in the form of

    [
        (tax_id1, rank1, name_txt1),
        (tax_id2, rank2, name_txt2),
        ...
    ]

    to a dict
    """
    dd = {}
    num_re = re.compile('[0-9]+')
    len_lineage = len(lineage)
    for k, __ in enumerate(lineage):
        tax_id, rank, name_txt = __
        # use the last rank as the tax_id, whatever it is, genus or species.
        if k == len_lineage - 1:
            dd['tax_id'] = tax_id

        # e.g. there could be multiple 'no rank'
        numbered_rank = rank
        while numbered_rank in dd:
            # print __, numbered_rank
            search = num_re.search(numbered_rank)
            if search is None:
                count = 1
            else:
                count = int(search.group()) + 1
            numbered_rank = '{0}{1}'.format(rank, count)
        dd[numbered_rank] = name_txt
    return dd


def find_lineage(tax_id):
    if tax_id % 50000 == 0:
        logging.debug('working on tax_id: {0}'.format(tax_id))
    lineage = []
    while True:
        rec = TAXONOMY_DICT[tax_id]
        lineage.append((rec['tax_id'], rec['rank'], rec['name_txt']))
        tax_id = rec['parent_tax_id']

        if tax_id == 1:
            break

    # reverse results in lineage of Kingdom => species, this is helpful for
    # to_dict when there are multiple "no rank"s
    lineage.reverse()
    return to_dict(lineage)


def main():
    # data downloaded from ftp://ftp.ncbi.nih.gov/pub/taxonomy/
    args = parse_args()
    nodes_df = load_nodes(args.nodes_file)
    names_df = load_names(args.names_file)
    df = nodes_df.merge(names_df, on='tax_id')
    df = df[['tax_id', 'parent_tax_id', 'rank', 'name_txt']]
    df.reset_index(drop=True, inplace=True)
    logging.info('# of tax ids: {0}'.format(df.shape[0]))
    # log summary info about the dataframe
    df.info()

    # force to use global variable TAXONOMY_DICT because map doesn't allow
    # passing extra args easily

    # TAXONOMY_DICT: a dict with tax_id as the key and each record as a value.
    # example tuple items:
    # (1,
    #  {'parent_tax_id': 1, 'name_txt': 'root',
    #   'rank': 'no rank', 'tax_id': 1}
    # )

    # (16,
    #  {'parent_tax_id': 32011, 'name_txt': 'Methylophilus',
    #   'rank': 'genus', 'tax_id': 16}
    # )

    global TAXONOMY_DICT
    logging.info('generating TAXONOMY_DICT...')
    TAXONOMY_DICT = dict(zip(df.tax_id.values, df.to_dict('records')))

    ncpus = multiprocessing.cpu_count()
    logging.info('found {0} cpus, and will use all of them to find lineages '
                 'for all tax ids'.format(ncpus))
    pool = multiprocessing.Pool(ncpus)
    # take about 18G memory
    lineages_dd = pool.map(find_lineage, df.tax_id.values)
    pool.close()

    logging.info('generating a dictionary of lineages information...')
    dd_for_df = dict(zip(range(len(lineages_dd)), lineages_dd))

    logging.info('generating lineages_df...')
    lineages_df = pd.DataFrame.from_dict(dd_for_df, orient='index')
    lineages_df.sort_values('tax_id', inplace=True)
    # # alternatively, but less useful, sort by ranks
    # lineages_df.sort_values(['superkingdom',
    #                          'phylum',
    #                          'class',
    #                          'order',
    #                          'family',
    #                          'genus',
    #                          'species'], inplace=True)

    lineages_csv_output = os.path.join('{0}.csv.gz'.format(args.output_prefix))
    backup_file(lineages_csv_output)
    logging.info("writing lineages to {0}".format(lineages_csv_output))
    with gzip.open(lineages_csv_output, 'wb') as opf:
        cols = ['tax_id',
                'superkingdom',
                'phylum',
                'class',
                'order',
                'family',
                'genus',
                'species']

        other_cols = sorted([__ for __ in lineages_df.columns
                             if __ not in cols])
        output_cols = cols + other_cols
        lineages_df.to_csv(opf, index=False, columns=output_cols)


if __name__ == "__main__":
    main()
