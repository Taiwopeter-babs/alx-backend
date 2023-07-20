#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import Dict, List, Union


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None,
                        page_size: int = 10
                        ) -> Dict[str, Union[List[List], int]]:
        """
        Returns a hypermedia with the next available index,
        that persists with deletion of data
        """
        next_index: int
        # This can also be the index depending on availability of the index
        # in storage
        index_to_show: int

        if index is None:
            index = 0

        # sort based on keys; which are integers
        dataset: Dict[int, List[str]] = dict(sorted(
            self.indexed_dataset().items(), key=lambda item: item[0]))

        # check for valid index
        assert index <= len(dataset) and index >= 0

        # check if index is available in data
        count = index
        while True:
            if dataset.get(count):
                index_to_show = count
                break
            count += 1

        # data for page to return
        data_list = [
            dataset.get(idx)
            for idx in range(index_to_show, index_to_show + page_size)
        ]
        # Get the next index for navigation
        # this could have been deleted
        probable_next_index = index_to_show + page_size

        while probable_next_index:
            if probable_next_index > len(dataset):
                next_index = None
                break
            # continue iteration if index is unavailable
            if not dataset.get(probable_next_index):
                probable_next_index += 1
                continue
            # set to next available index
            next_index = probable_next_index
            break

        return {
            "index": index if index else 0,
            "data": data_list,
            "next_index": next_index,
            "page_size": page_size
        }
