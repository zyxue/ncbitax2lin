"""Data strutures."""

from typing import List, NewType, Tuple

from typing_extensions import TypedDict


class TaxUnit(TypedDict):
    """
    Represents a basic unit in taxonomy e.g. (phylum, Proteobacteria), where
    phylum is the rank, and Proteobacteria is the rank name
    """

    tax_id: int
    parent_tax_id: int  # tax_id of parent tax unit for this tax unit
    rank: str
    rank_name: str


# A lineage is a list of (tax_id, rank, rank_name) tuples.
Lineage = NewType("Lineage", List[Tuple[int, str, str]])
