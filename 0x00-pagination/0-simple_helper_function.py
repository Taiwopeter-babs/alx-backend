#!/usr/bin/env python3
"""Helper function"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int]:
    """returns the index range for a page in a tuple
    Args:
      page(int): Current page number

      page_size(int): Amount of items page can show
    """
    # upper index limit of items on the page
    upper_bound = page_size * page
    # starting index of items on the page
    lower_bound = upper_bound - page_size

    return (lower_bound, upper_bound)
