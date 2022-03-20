"""Converts NCBI taxonomy dump into lineages"""

import logging
import sys
from typing import Dict, Optional

import fire
import pandas as pd

from ncbitax2lin import data_io, fmt, lineage, utils
from ncbitax2lin.struct import TaxUnit

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s|%(levelname)s|%(message)s")


_LOGGER = logging.getLogger(__name__)


def _calc_taxonomy_dict(df_tax: pd.DataFrame) -> Dict[int, TaxUnit]:
    """Converts dataframe of df_tax into a dictionary with tax_id as the keys"""
    return dict(zip(df_tax.tax_id.values, df_tax.to_dict("records")))


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

    _LOGGER.info("Generating a dictionary of taxonomy: tax_id => tax_unit ...")
    tax_dict = _calc_taxonomy_dict(df_data)

    tax_dict_size_mb = sys.getsizeof(tax_dict) / 2**20
    _LOGGER.info("size of taxonomy_dict: ~%s MB", f"{tax_dict_size_mb:.0f}")

    tax_ids = df_data.tax_id.to_numpy().tolist()

    _LOGGER.info("Finding all lineages ...")
    all_lineages = lineage.find_all_lineages(tax_ids, tax_dict)

    _LOGGER.info("Preparings all lineages into a dataframe to be written to disk ...")
    df_lineages = fmt.prepare_lineages_for_output(all_lineages)

    if output is None:
        output = f"ncbi_lineages_{pd.Timestamp.utcnow().date()}.csv.gz"

    utils.maybe_backup_file(output)

    _LOGGER.info("Writing lineages to %s ...", output)
    data_io.write_lineages_to_disk(df_lineages, output)


def main() -> None:
    """Main function, entry point"""
    fire.Fire(taxonomy_to_lineages)
