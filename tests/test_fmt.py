"""tests for fmt.py"""
# pylint: disable=missing-function-docstring, protected-access
from typing import Container

import pytest

from ncbitax2lin import fmt


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
def test__calc_rank_key(
    test_input_rank: str, test_input_existing_ranks: Container[str], expected: str
) -> None:
    actual = fmt._calc_rank_key(test_input_rank, test_input_existing_ranks)
    assert actual == expected
