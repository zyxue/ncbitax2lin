"""tests for data_reader.py"""
# pylint: disable=protected-access, missing-function-docstring

from typing import Container

import pandas as pd
import pytest

from ncbitax2lin import ncbitax2lin


@pytest.mark.parametrize(
    "test_input_rank, test_input_existing_ranks, expected",
    [
        ("no rank", {}, "no rank"),
        ("no rank", {"some other rank"}, "no rank"),
        ("no rank", {"no rank"}, "no rank1"),
        ("rankx", ["rankx"], "rankx1"),
        ("rankx", ["rankx", "rankx1"], "rankx2"),
    ],
)
def test_calc_rank_key(
    test_input_rank: str, test_input_existing_ranks: Container[str], expected: str
) -> None:
    assert (
        ncbitax2lin.calc_rank_key(test_input_rank, test_input_existing_ranks)
        == expected
    )


def test_calc_taxonomy_dict() -> None:
    df_data = pd.DataFrame(
        {
            "tax_id": [1, 2, 6],
            "parent_tax_id": [1, 131567, 335928],
            "rank": ["no rank", "superkingdom", "genus"],
            "rank_name": ["root", "Bacteria", "Azorhizobium",],
        }
    )

    actual = ncbitax2lin.calc_taxonomy_dict(df_data)
    expected = {
        1: {"tax_id": 1, "parent_tax_id": 1, "rank": "no rank", "rank_name": "root"},
        2: {
            "tax_id": 2,
            "parent_tax_id": 131567,
            "rank": "superkingdom",
            "rank_name": "Bacteria",
        },
        6: {
            "tax_id": 6,
            "parent_tax_id": 335928,
            "rank": "genus",
            "rank_name": "Azorhizobium",
        },
    }

    assert actual == expected
