#!/usr/bin/env python3
"""
Pagination module
"""
import csv
import math
from typing import Dict, List, Tuple, Union


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def index_range(self, page: int, page_size: int) -> Tuple[int]:
        """
        ### returns the index range for a page in a tuple
        Args:
          page(int): Current page number

          page_size(int): Amount of items page can show
        """
        # upper index limit of items on the page
        upper_bound = page_size * page

        # starting index of items on the page
        lower_bound = upper_bound - page_size

        return (lower_bound, upper_bound)

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        returns paginated items for a page
        """

        lower_idx: int
        upper_idx: int

        # Check arguments
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0

        # get upper and lower bounds
        lower_idx, upper_idx = self.index_range(page, page_size)
        if lower_idx > len(self.dataset()):
            return []

        items_to_return = self.dataset()[lower_idx:upper_idx]

        return items_to_return

    def get_hyper(self, page: int = 1,
                  page_size: int = 10
                  ) -> Dict[str, Union[int, None, List[List]]]:
        """
        return hypermedia for the paginated application
        """
        # total pages to be returned
        total_pages: int = math.ceil(len(self.dataset()) / page_size)

        next_page_num: Union[int, None]
        prev_page_num: Union[int, None]

        # next page number
        if page + 1 <= total_pages:
            next_page_num = page + 1
        else:
            next_page_num = None

        # previous page number
        if page == 1:
            prev_page_num = None
        else:
            prev_page_num = page - 1

        return {
            "page_size": page_size,
            "page": page,
            "data": self.get_page(page, page_size),
            "next_page": next_page_num,
            "prev_page": prev_page_num,
            "total_pages": total_pages
        }
