#!/usr/bin/env python3
"""
LIFOCache Module
"""
from typing import Any

# BaseCaching class
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """FIFO caching class system"""

    def __init__(self):
        """Intialize class method"""
        super().__init__()

    def put(self, key, item: Any):
        """
        Adds an item to the cache storage, and removes the
        first item if the size of the cache storage is exceeded (FIFO)
        """
        # key to remove if cache storage is full
        last_key: str
        cache_size: int

        if key and item:
            cache_size = len(self.cache_data)

            # check for cache capacity
            if cache_size == self.MAX_ITEMS:

                # remove existing key
                if self.cache_data.get(key):
                    del self.cache_data[key]
                else:
                    # get the last key in cache storage
                    last_key = list(self.cache_data.keys())[-1]
                    print('DISCARD: {}'.format(last_key))

                    # delete from cache, LIFO
                    del self.cache_data[last_key]

            self.cache_data[key] = item

    def get(self, key) -> Any:
        """Gets an item from the cache"""
        if key is None or self.cache_data.get(key) is None:
            return None
        return self.cache_data.get(key)
