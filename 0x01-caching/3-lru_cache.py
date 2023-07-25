#!/usr/bin/env python3
"""
LRUCache Module
"""
from typing import Any, Dict


# BaseCaching class
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """Least Recently Used (LRU) caching class system"""

    def __init__(self):
        """Intialize class method"""
        super().__init__()

    def put(self, key, item: Any):
        """
        Adds an item to the cache storage, and removes the item
        at the first index of dict.keys() list; it is the least
        recently used
        """
        # key to remove: least recently used
        key_to_del: str
        cache_size: int

        if not key or not item:
            return

        cache_size = len(self.cache_data)

        # check for cache capacity
        if cache_size == self.MAX_ITEMS:

            # remove existing key; added to the front of the queue
            if self.cache_data.get(key):
                del self.cache_data[key]

            # delete the key at the back of the queue
            # It is the least recently used
            else:
                key_to_del = list(self.cache_data.keys())[0]
                print('DISCARD: {}'.format(key_to_del))

                # delete from cache, LRU
                del self.cache_data[key_to_del]

        # add key with new item to the front of the queue
        self.cache_data[key] = item

    def get(self, key) -> Any:
        """Gets an item from the cache"""
        if key is None or self.cache_data.get(key) is None:
            return None

        # move key to the front of the queue
        key_value = self.cache_data.get(key)
        del self.cache_data[key]
        self.cache_data[key] = key_value

        return self.cache_data.get(key)
