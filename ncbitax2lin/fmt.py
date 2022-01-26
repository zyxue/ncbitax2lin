"""Utilities for preparing the lineages for output."""

import concurrent.futures
from typing import Container, Dict, List, Union

import pandas as pd

from ncbitax2lin.struct import Lineage


def _calc_rank_key(rank: str, existing_ranks: Container[str]) -> str:
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


def _convert_lineage_to_dict(lineage: Lineage) -> Dict[str, Union[int, str]]:
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

        rank_key = _calc_rank_key(rank, output.keys())
        output[rank_key] = rank_name
    return output


def prepare_lineages_for_output(lineages: List[Lineage]) -> pd.DataFrame:
    """prepares lineages into a dataframe for writing to disk"""

    with concurrent.futures.ProcessPoolExecutor() as executors:
        out = executors.map(_convert_lineage_to_dict, lineages, chunksize=5000)

    df_out = pd.DataFrame(out)

    return df_out.sort_values("tax_id")
