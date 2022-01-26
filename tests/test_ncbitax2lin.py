"""tests for ncbitax2lin.py"""
# pylint: disable=protected-access, missing-function-docstring


import pandas as pd

from ncbitax2lin import ncbitax2lin


def test__calc_taxonomy_dict() -> None:
    df_data = pd.DataFrame(
        {
            "tax_id": [1, 2, 6],
            "parent_tax_id": [1, 131567, 335928],
            "rank": ["no rank", "superkingdom", "genus"],
            "rank_name": ["root", "Bacteria", "Azorhizobium",],
        }
    )

    actual = ncbitax2lin._calc_taxonomy_dict(df_data)
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
