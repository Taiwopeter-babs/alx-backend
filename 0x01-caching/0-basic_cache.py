#!/usr/bin/env python3
"""
BasicCache Module
"""

# BaseCaching class
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """
    BaseCache class that implements basic caching.
    This class inherits from the BasicCaching class
    """

    def __init__(self):
        """Intialize class method"""
        super().__init__()

    def put(self, key, item):
        """Adds an item to the cache storage"""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """Gets an item from the cache"""
        if key is None or self.cache_data.get(key) is None:
            return None
        return self.cache_data.get(key)
