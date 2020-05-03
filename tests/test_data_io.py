"""tests for data_reader.py"""
# pylint: disable=protected-access, missing-function-docstring

from pathlib import Path

import pandas as pd

from ncbitax2lin import data_io


def test_load_nodes() -> None:
    # top 20 lines of nodes.dmp from NCBI
    test_input = (Path(__file__).parent / "./test_data/nodes.head_20.dmp").as_posix()
    actual = data_io.load_nodes(test_input)
    assert isinstance(actual, pd.DataFrame)


def test_load_names() -> None:
    # top 20 lines of names.dmp from NCBI
    test_input = (Path(__file__).parent / "./test_data/names.head_20.dmp").as_posix()
    actual = data_io.load_names(test_input)
    assert isinstance(actual, pd.DataFrame)
