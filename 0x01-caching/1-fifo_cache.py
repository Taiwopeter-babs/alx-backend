#!/usr/bin/env python3
"""
FIFOCache Module
"""
from typing import Any

# BaseCaching class
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """FIFO caching class system"""

    def __init__(self):
        """Intialize class method"""
        super().__init__()

    def put(self, key, item):
        """
        Adds an item to the cache storage, and removes the
        first item if the size of the cache storage is exceeded (FIFO)
        """
        # key to remove if cache storage is full
        first_key: str

        if not key or not item:
            return
        # check for cache capacity
        if len(self.cache_data) == self.MAX_ITEMS:
            # Only new keys will cause a deletion
            if self.get(key) is None:
                first_key = list(self.cache_data.keys())[0]
                print('DISCARD: {}'.format(first_key))

                # delete from cache, FIFO
                del self.cache_data[first_key]

        self.cache_data[key] = item

    def get(self, key):
        """Gets an item from the cache"""
        if key is None or self.cache_data.get(key) is None:
            return None
        return self.cache_data.get(key)
