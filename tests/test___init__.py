"""tests for __init__.py"""
# pylint: disable=protected-access, missing-function-docstring
from ncbitax2lin import __version__


def test_version() -> None:
    assert __version__ == "2.0"
