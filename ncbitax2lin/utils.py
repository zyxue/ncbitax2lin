"""Utility functions"""

import datetime
import functools
import io
import logging
import os
import time
from typing import Any, Callable, List, TypeVar

import pandas as pd

_LOGGER = logging.getLogger(__name__)


def timeit(func: Callable[..., Any]) -> Callable[..., Any]:
    """Times a function, usually used as decorator"""

    @functools.wraps(func)
    def timed_func(*args: Any, **kwargs: Any) -> Any:
        """Returns the timed function"""
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = datetime.timedelta(seconds=(time.time() - start_time))
        _LOGGER.info("time spent on %s: %s", func.__name__, elapsed_time)
        return result

    return timed_func


def maybe_backup_file(filepath: str) -> None:
    """
    Back up a file, old_file will be renamed to #old_file.n#, where n is a
    number incremented each time a backup takes place
    """
    backup = None
    if os.path.exists(filepath):
        dirname = os.path.dirname(filepath)
        basename = os.path.basename(filepath)
        count = 1
        backup = os.path.join(dirname, f"#{basename}.{count}#")
        while os.path.exists(backup):
            count += 1
            backup = os.path.join(dirname, f"#{basename}.{count}#")
        logging.info("Backing up %s to %s", filepath, backup)
        os.rename(filepath, backup)


ElemType = TypeVar("ElemType")


def partition(vals: List[ElemType], size: int) -> List[List[ElemType]]:
    """Partion a list into a list of lists by size."""
    return [vals[i : i + size] for i in range(0, len(vals), size)]


def collect_df_info(df_data: pd.DataFrame) -> str:
    """Collects information of a dataframe"""
    buf = io.StringIO()
    df_data.info(buf=buf, verbose=True, memory_usage="deep")
    return buf.getvalue()
