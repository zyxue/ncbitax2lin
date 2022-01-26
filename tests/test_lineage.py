"""tests for lineage.py"""
# pylint: disable=missing-function-docstring, protected-access

from unittest.mock import MagicMock, patch

import pytest

from ncbitax2lin import lineage


@patch("multiprocessing.cpu_count", return_value=999, autospec=True)
def test__calc_num_procs(mock_cpu_count: MagicMock) -> None:
    actual = lineage._calc_num_procs()
    expected = 6
    assert actual == expected
    mock_cpu_count.assert_called_once_with()


@pytest.mark.parametrize(
    "num_vals, num_chunks, chunk_size",
    [
        (10, 3, 4),
        (11, 3, 4),
        (12, 3, 4),
        (13, 3, 5),
        (14, 3, 5),
        (15, 3, 5),
        (16, 3, 6),
    ],
)
def test__calc_chunk_size_procs(
    num_vals: int, num_chunks: int, chunk_size: int
) -> None:
    actual = lineage._calc_chunk_size(num_vals, num_chunks)
    expected = chunk_size
    assert actual == expected
    assert isinstance(chunk_size, int)
