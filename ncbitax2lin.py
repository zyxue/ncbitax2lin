import re
import os
import gzip
import multiprocessing
import argparse
import logging
import shelve
import pandas as pd

from utils import timeit


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
        help='will output lineage name information in output_prefix.csv.gz')

    parser.add_argument(
        '--names-output-prefix', default='ncbi_names',
        help='will output scientific-name information in names_output_prefix.csv.gz')

    parser.add_argument(
        '--common-names-output-prefix', default='ncbi_common_names',
        help='will output common-name information in common_names_output_prefix.csv.gz')

    parser.add_argument(
        '--taxid-lineages-output-prefix', default='ncbi_taxid_lineages',
        help='will output lineage taxon-ID information in taxid_lineages_output_prefix.csv.gz')

    args = parser.parse_args()
    return args


def strip(str_):
    '''
    :param str_: a string
    '''
    return str_.strip()


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
    df['rank'] = df['rank'].apply(strip)
    df['embl_code'] = df['embl_code'].apply(strip)
    df['comments'] = df['comments'].apply(strip)
    return df


@timeit
def load_names(names_file, name_class='scientific name'):
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
    df['name_txt'] = df['name_txt'].apply(strip)
    df['unique_name'] = df['unique_name'].apply(strip)
    df['name_class'] = df['name_class'].apply(strip)

    sci_df = df[df['name_class'] == name_class]
    sci_df.reset_index(drop=True, inplace=True)
    return sci_df


def to_name_dict(lineage):
    """
    convert the lineage from a list of tuples in the form of

    [
        (tax_id1, rank1, name_txt1),
        (tax_id2, rank2, name_txt2),
        ...
    ]

    to a dictionary of taxon names
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

def to_taxid_dict(lineage):
    """
    convert the lineage from a list of tuples in the form of
    [
        (tax_id1, rank1, name_txt1),
        (tax_id2, rank2, name_txt2),
        ...
    ]
    to a dictionary of taxids
    """
    dd = {}
    num_re = re.compile('[0-9]+')
    len_lineage = len(lineage)
    for k, __ in enumerate(lineage):
        tax_id, rank, name_txt = __
        # use the last rank as the tax_id, whatever it is, genus or species.
        if k == len_lineage - 1:
            dd['tax_id'] = int(tax_id)

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
        dd[numbered_rank] = int(tax_id)
    return dd

def find_lineage(tax_id):
    if tax_id % 50000 == 0:
        logging.debug('working on tax_id: {0}'.format(tax_id))
    lineage = []
    while True:
        rec = TAXONOMY_DICT[tax_id]
        print "%s, %s" % (str(tax_id), rec)
        lineage.append((rec['tax_id'], rec['rank'], rec['name_txt']))
        tax_id = rec['parent_tax_id']

        if tax_id == 1:
            break

    # reverse results in lineage of Kingdom => species, this is helpful for
    # to_dict when there are multiple "no rank"s
    lineage.reverse()
    return to_name_dict(lineage), to_taxid_dict(lineage)

def process_lineage_dd(lineage_dd):
    dd_for_df = dict(zip(range(len(lineage_dd)), lineage_dd))
    lineages_df = pd.DataFrame.from_dict(dd_for_df, orient='index')
    return lineages_df.sort_values('tax_id')

def write_output(output_prefix, output_name_log, df, cols=None, undef_taxids=None):
    output = os.path.join('{0}.csv.gz'.format(output_prefix))
    logging.info("writing %s to %s" % (output_name_log, output))
    with open(output, 'wb') as opf:
        # make sure the name and timestamp are not gzipped, (like gzip -n)
        opf_gz = gzip.GzipFile('', 'wb', 9, opf, 0.)
        if undef_taxids and cols:
            for col in undef_taxids.keys():
                df[[col]] = df[[col]].fillna(value=undef_taxids[col])
            df[cols] = df[cols].astype(int)
        if cols:
            df.to_csv(opf_gz, index=False, columns=cols)
        else:
            df.to_csv(opf_gz, index=False)
        opf_gz.close()

def generate_outputs(nodes_file, names_file, name_class, names_output_prefix, taxid_lineages_output_prefix=None):
    nodes_df = load_nodes(nodes_file)
    names_df = load_names(names_file, name_class)
    df = nodes_df.merge(names_df, on='tax_id')
    df = df[['tax_id', 'parent_tax_id', 'rank', 'name_txt']]
    df.reset_index(drop=True, inplace=True)
    logging.info('# of tax ids: {0}'.format(df.shape[0]))
    df.info()

    global TAXONOMY_DICT # example item: (16, {'parent_tax_id': 32011, 'name_txt': 'Methylophilus', 'rank': 'genus', 'tax_id': 16})
    logging.info('generating TAXONOMY_DICT...')
    TAXONOMY_DICT = dict(zip(df.tax_id.values, df.to_dict('records')))

    ncpus = multiprocessing.cpu_count()
    logging.info('found {0} cpus, and will use all of them to find lineages '
                 'for all tax ids'.format(ncpus))
    pool = multiprocessing.Pool(ncpus)
    name_lineages_dd, taxid_lineages_dd = zip(*pool.map(find_lineage, df.tax_id.values)) # take about 18G memory
    pool.close()

    logging.info('generating names output...')
    write_output(names_output_prefix, "names", df, ['tax_id', 'name_txt'])

    if taxid_lineages_output_prefix:
        logging.info('generating lineage-by-taxid output...')
        taxid_lineages_df = process_lineage_dd(taxid_lineages_dd)
        undef_taxids = {'species': -100,
                        'genus': -200,
                        'family': -300,
                        'order': -400,
                        'class': -500,
                        'phylum': -600,
                        'superkingdom': -700}
        write_output(taxid_lineages_output_prefix, "taxid lineages", taxid_lineages_df,
                     ['tax_id', 'superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'],
                     undef_taxids)

        logging.info('writing lineage-by-taxid shelf...')
        taxid_lineages_shelf_output = os.path.join('{0}.db'.format(taxid_lineages_output_prefix))
        d = shelve.open(taxid_lineages_shelf_output)
        for index, row in taxid_lineages_df.iterrows():
            d[str(int(row['tax_id']))] = (str(int(row['species'])), str(int(row['genus'])), str(int(row['family'])))
        d.close()

def main():
    args = parse_args()
    logging.info('PART I: common name output')
    generate_outputs(args.nodes_file, args.names_file, 'genbank common name', args.common_names_output_prefix)
    logging.info('PART II: lineage and scientific name outputs')
    generate_outputs(args.nodes_file, args.names_file, 'scientific name', args.names_output_prefix,
                     args.taxid_lineages_output_prefix)

if __name__ == "__main__":
    main()
