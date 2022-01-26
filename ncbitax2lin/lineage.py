"""Utilities for finding lineages."""

import logging
import math
import multiprocessing
import pickle
import tempfile
from typing import Dict, List

from ncbitax2lin import utils
from ncbitax2lin.struct import Lineage, TaxUnit

_LOGGER = logging.getLogger(__name__)

# tax_id of first line in names.dmp: no rank
ROOT_TAX_ID = 1


def _find_one_lineage(tax_id: int, tax_dict: Dict[int, TaxUnit]) -> Lineage:
    """Finds lineage for a single tax id"""
    if tax_id % 50000 == 0:
        # TODO: it's tricky why _LOGGER.info here won't make the log show up.
        # Note, this function is run in a subprocess.
        print(f"working on tax_id: {tax_id}")

    lineage = []
    while True:
        record = tax_dict[tax_id]
        lineage.append((record["tax_id"], record["rank"], record["rank_name"]))
        tax_id = record["parent_tax_id"]

        # every tax can be traced back to tax_id == 1, the root
        if tax_id == ROOT_TAX_ID:
            break

    # reverse results in lineage of Kingdom => species, this is helpful for
    # to_dict when there are multiple "no rank"s
    lineage.reverse()
    return Lineage(lineage)


def _find_lineages(
    tax_ids: List[int], tax_dict: Dict[int, TaxUnit], output: str
) -> None:
    """Finds lineages for a list of tax ids."""

    lineages = []
    for tax_id in tax_ids:
        lineage = _find_one_lineage(tax_id, tax_dict)
        lineages.append(lineage)

    with open(output, "wb") as opened:
        pickle.dump(lineages, opened)


def _calc_num_procs(max_num: int = 6) -> int:
    """Calculates number of the processes to use."""
    return min(multiprocessing.cpu_count(), max_num)


def _calc_chunk_size(num_vals: int, num_chunks: int) -> int:
    """Calculates the chunk size."""
    return math.ceil(num_vals / num_chunks)


def find_all_lineages(
    tax_ids: List[int], tax_dict: Dict[int, TaxUnit]
) -> List[Lineage]:
    """Finds the lineages for all tax ids

    Args:
        tax_id: all tax ids to find lineages for.
        tax_dict: a dictionary of tax_id => tax_unit.
    """
    nprocs = _calc_num_procs()
    _LOGGER.info("will use %d processes to find lineages for all tax ids", nprocs)

    chunk_size = _calc_chunk_size(len(tax_ids), num_chunks=nprocs)
    _LOGGER.info("chunk_size = %d", chunk_size)

    tax_id_chunks = utils.partition(tax_ids, size=chunk_size)
    _LOGGER.info("chunked sizes: %s", [len(_) for _ in tax_id_chunks])

    procs, tmp_outputs, all_lineages = [], [], []

    with tempfile.TemporaryDirectory(suffix="_ncbitax2lin") as tmpdir:
        for index, chunk in enumerate(tax_id_chunks):
            tmp_output = f"/{tmpdir}/_lineages_{index}.pkl"

            tmp_outputs.append(tmp_output)
            proc = multiprocessing.Process(
                target=_find_lineages, args=(chunk, tax_dict, tmp_output)
            )
            procs.append(proc)

        _LOGGER.info("Starting %d processes ...", len(procs))
        for proc in procs:
            proc.start()

        _LOGGER.info("Joining %d processes ...", len(procs))
        for proc in procs:
            proc.join()

        for tmp_output in tmp_outputs:
            _LOGGER.info("adding lineages from %s ...", tmp_output)
            with open(tmp_output, "rb") as opened:
                all_lineages.extend(pickle.load(opened))

    assert len(all_lineages) == len(tax_ids), (
        f"There are {len(tax_ids)} tax_ids, but {len(all_lineages)} lineages are generated, "
        "the two numbers should've been the same"
    )
    return all_lineages
