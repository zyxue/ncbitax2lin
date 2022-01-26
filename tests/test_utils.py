"""tests for utils.py"""
# pylint: disable=protected-access, missing-function-docstring

import os
from typing import List
from unittest.mock import MagicMock, call, patch

import pytest

from ncbitax2lin import utils


def test_maybe_backup_file_when_file_path_does_not_exist() -> None:
    with patch("os.path.exists", return_value=False) as mock_exists:
        test_input = "some_non_existing_file"
        utils.maybe_backup_file(test_input)
        mock_exists.assert_called_once_with(test_input)


@patch("os.rename", spec=os.rename)
@patch("os.path.exists")
def test_maybe_backup_file_when_file_path_exists(
    mock_exists: MagicMock, mock_rename: MagicMock
) -> None:
    mock_exists.side_effect = [True, False]
    test_input = "some_existing_file"

    utils.maybe_backup_file(test_input)
    expected = "#some_existing_file.1#"

    assert mock_exists.has_calls(call(test_input), call(expected))
    mock_rename.assert_called_once_with(test_input, expected)


@patch("os.rename", spec=os.rename)
@patch("os.path.exists")
def test_maybe_backup_file_when_backfile_also_exists(
    mock_exists: MagicMock, mock_rename: MagicMock
) -> None:
    mock_exists.side_effect = [True, True, False]
    test_input = "some_existing_file"
    intermediary_input = "#some_existing_file.1#"

    utils.maybe_backup_file(test_input)
    expected = "#some_existing_file.2#"

    assert mock_exists.has_calls(
        call(test_input), call(intermediary_input), call(expected)
    )
    mock_rename.assert_called_once_with(test_input, expected)


@pytest.mark.parametrize(
    "test_input, size, expected",
    [
        ([1, 2, 3], 3, [[1, 2, 3]]),
        ([1, 2, 3], 2, [[1, 2], [3]]),
        ([1, 2, 3, 4], 2, [[1, 2], [3, 4]]),
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([1, 2, 3, 4, 5], 3, [[1, 2, 3], [4, 5]]),
    ],
)
def test__partition(
    test_input: List[int], size: int, expected: List[List[int]],
) -> None:
    actual = utils.partition(test_input, size)
    assert actual == expected
