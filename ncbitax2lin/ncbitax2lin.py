"""Converts NCBI taxonomy dump into lineages"""

import logging
import multiprocessing
from typing import Container, Dict, Iterable, List, Optional, Union

import fire
import pandas as pd

from ncbitax2lin import data_io, utils
from ncbitax2lin.struct import Lineage, TaxUnit

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s|%(levelname)s|%(message)s")


_LOGGER = logging.getLogger(__name__)


# set TAXONOMY_DICT as global variable so it can work with multiprocess.Pool
# more easily
TAXONOMY_DICT: Dict[int, TaxUnit] = {}

# tax_id of first line in names.dmp: no rank
ROOT_TAX_ID = 1


def calc_rank_key(rank: str, existing_ranks: Container[str]) -> str:
    """Calcluates a key for the lineage representation in a dictionary.

    Defaults to the rank itself, e.g. no rank, superkingdom, phylum, etc. but
    when a rank appears multiple times (common for "no rank" rank) in a single
    linearge it will be numbered, e.g. no rank1, no rank2, and so on.

    Args:
        rank: e.g. no rank, superkingdom, phylum, etc.
        existing_ranks: rank keys already existing
    """
    # e.g. there could be multiple 'no rank'
    if rank not in existing_ranks:
        return rank

    count = 1
    numbered_rank = f"{rank}{count}"
    while numbered_rank in existing_ranks:
        count += 1
        numbered_rank = f"{rank}{count}"
    return numbered_rank


def calc_taxonomy_dict(df_tax: pd.DataFrame) -> Dict[int, TaxUnit]:
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


def convert_lineage_to_dict(lineage: Lineage) -> Dict[str, Union[int, str]]:
    """Converts the lineage in a list-of-tuples represetantion to a dictionary representation

    [
        ("tax_id1", "rank1", "name_txt1"),
        ("tax_id2", "rank2", "name_txt2"),
        ...
    ]

    becomes

    {
        "rank1": "name_txt1",
        "rank2": "name_txt2",
        "tax_id": "tax_id2",   # using the last rank as the tax_id of this lineage
    }

    A concrete example:

        [
            (131567, 'no rank', 'cellular organisms'),
            (2, 'superkingdom', 'Bacteria')
        ]

    becomes

        {
            'no rank': 'cellular organisms',
            'superkingdom': 'Bacteria',
            'tax_id': 2,
        }

    """
    output: Dict[str, Union[int, str]] = {}
    len_lineage = len(lineage)
    for k, (tax_id, rank, rank_name) in enumerate(lineage):
        # use the last rank of the lineage as the tax_id of the lineage
        if k == len_lineage - 1:
            output["tax_id"] = tax_id

        rank_key = calc_rank_key(rank, output.keys())
        output[rank_key] = rank_name
    return output


def prepare_lineages_for_output(lineages: List[Lineage]) -> pd.DataFrame:
    """prepares lineages into a dataframe for writing to disk"""
    _LOGGER.info("Preparings all lineages into a dataframe to be written to disk ...")

    df_out = pd.DataFrame([convert_lineage_to_dict(lineage) for lineage in lineages])

    return df_out.sort_values("tax_id")


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
    TAXONOMY_DICT = calc_taxonomy_dict(df_data)

    lineages = find_all_lineages(df_data.tax_id)

    df_lineages = prepare_lineages_for_output(lineages)

    if output is None:
        output = f"ncbi_lineages_{pd.Timestamp.utcnow().date()}.csv.gz"
    utils.maybe_backup_file(output)
    _LOGGER.info("Writing lineages to %s ...", output)
    data_io.write_lineages_to_disk(df_lineages, output)


def main() -> None:
    """Main function, entry point"""
    fire.Fire(taxonomy_to_lineages)
