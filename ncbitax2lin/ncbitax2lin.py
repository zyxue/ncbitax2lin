"""Converts NCBI taxonomy dump into lineages"""

import logging
import multiprocessing
from typing import Dict, Iterable, List, Optional

import fire
import pandas as pd

from ncbitax2lin import data_io, fmt, utils
from ncbitax2lin.struct import Lineage, TaxUnit

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s|%(levelname)s|%(message)s")


_LOGGER = logging.getLogger(__name__)


# set TAXONOMY_DICT as global variable so it can work with multiprocess.Pool
# more easily
TAXONOMY_DICT: Dict[int, TaxUnit] = {}

# tax_id of first line in names.dmp: no rank
ROOT_TAX_ID = 1


def _calc_taxonomy_dict(df_tax: pd.DataFrame) -> Dict[int, TaxUnit]:
    """Converts dataframe of df_tax into a dictionary with tax_id as the keys"""
    return dict(zip(df_tax.tax_id.values, df_tax.to_dict("records")))


def find_lineage(tax_id: int) -> Lineage:
    """Finds lineage for a single tax id"""
    if tax_id % 50000 == 0:
        _LOGGER.info("working on tax_id: %d", tax_id)

    lineage = []
    while True:
        record = TAXONOMY_DICT[tax_id]
        lineage.append((record["tax_id"], record["rank"], record["rank_name"]))
        tax_id = record["parent_tax_id"]

        # every tax can be traced back to tax_id == 1, the root
        if tax_id == ROOT_TAX_ID:
            break

    # reverse results in lineage of Kingdom => species, this is helpful for
    # to_dict when there are multiple "no rank"s
    lineage.reverse()
    return Lineage(lineage)


def find_all_lineages(tax_ids: Iterable) -> List[Lineage]:
    """Finds the lineages for all tax ids"""
    ncpus = multiprocessing.cpu_count()
    _LOGGER.info(
        "found %d cpus, and will use all of them to find lineages for all tax ids",
        ncpus,
    )

    with multiprocessing.Pool(ncpus) as pool:
        return pool.map(find_lineage, tax_ids)


def taxonomy_to_lineages(
    nodes_file: str, names_file: str, output: Optional[str] = None
) -> None:
    """Converts NCBI taxomony dump into lineages.

    NCBI taxonomy dump can be downloaded from
    ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz

    Args:
        nodes_file: path/to/taxdump/nodes.dmp from NCBI taxonomy
        names_file: path/to/taxdump/names.dmp from NCBI taxonomy
        output_prefix: output lineages will be written to output_prefix.csv.gz
    """
    df_data = data_io.read_names_and_nodes(names_file, nodes_file)
    _LOGGER.info("# of tax ids: %s", f"{df_data.shape[0]:,d}")
    _LOGGER.info("df.info:\n%s", f"{utils.collect_df_info(df_data)}")

    _LOGGER.info("Generating TAXONOMY_DICT ...")
    global TAXONOMY_DICT  # pylint: disable=global-statement
    TAXONOMY_DICT = _calc_taxonomy_dict(df_data)

    lineages = find_all_lineages(df_data.tax_id)

    _LOGGER.info("Preparings all lineages into a dataframe to be written to disk ...")
    df_lineages = fmt.prepare_lineages_for_output(lineages)

    if output is None:
        output = f"ncbi_lineages_{pd.Timestamp.utcnow().date()}.csv.gz"
    utils.maybe_backup_file(output)
    _LOGGER.info("Writing lineages to %s ...", output)
    data_io.write_lineages_to_disk(df_lineages, output)


def main() -> None:
    """Main function, entry point"""
    fire.Fire(taxonomy_to_lineages)
