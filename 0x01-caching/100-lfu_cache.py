#!/usr/bin/env python3
"""
LFUCache Module
"""
from typing import Any, Dict, List


# BaseCaching class
BaseCaching = __import__('base_caching').BaseCaching

# tracker for key access count
key_track: Dict[str, Any] = {}


class LFUCache(BaseCaching):
    """Least Frequently Used (LRU) caching class system"""

    def __init__(self):
        """Intialize class method"""
        super().__init__()

    def put(self, key, item: Any):
        """
        Adds an item to the cache storage, and removes the item
        at the first index of dict.keys() list; it is the least
        recently used
        """
        # cache storage size
        cache_size: int

        if not key or not item:
            return

        cache_size = len(self.cache_data)

        # check for cache capacity
        if cache_size == self.MAX_ITEMS:

            # get all keys likely to be removed
            possible_keys = self.keys_to_remove()

            # remove existing key; added to the front of the queue
            # in case of a multiple-key match of usage count in tracker
            if self.cache_data.get(key):
                del self.cache_data[key]

                # increment value of key in tracker
                key_track[key] += 1
                # print("UPDATE [[{}]]".format(key))
                # print("[[{}]] INCREASED".format(key))

            else:
                """
                Utilizes the LRU caching method if there are
                multiple keys with the same usage count in the tracker,
                thus the first key is removed from the cache storage as it
                will be the least recently used, otherwise the key with
                least count in the tracker `key_track` is removed
                """
                for key_del in list(self.cache_data.keys()):
                    if key_del in possible_keys:
                        # print(key_del, 'Key to be deleted')
                        print('DISCARD: {}'.format(key_del))
                        # remove the key from the cache
                        del self.cache_data[key_del]

                        # remove the key from the tracker
                        del key_track[key_del]

                        break

        # add key with new item to the front of the queue
        self.cache_data[key] = item
        # print("ADD/UPDATE [[{}]]".format(key))

        # add new keys to tracker
        if key_track.get(key) is None:
            key_track[key] = 0
        # print(key_track)

    def get(self, key) -> Any:
        """Gets an item from the cache"""
        if key is None or self.cache_data.get(key) is None:
            return None

        # increment key in tracker
        try:
            key_track[key] += 1
            # print("[[{}]] INCREASED".format(key))
        except KeyError:
            pass

        # move key to the front of the queue
        key_value = self.cache_data.get(key)
        del self.cache_data[key]
        self.cache_data[key] = key_value

        return self.cache_data.get(key)

    @staticmethod
    def keys_to_remove() -> List[str]:
        """
        returns a list of keys for removal from
        the cache
        """
        # list of values in tracker
        val_list = list(key_track.values())
        # list of keys
        key_list = list(key_track.keys())

        # find the minimum value
        min_val = val_list[0]
        for idx, num in enumerate(val_list):
            if idx == 0:
                continue
            if min_val >= num:
                min_val = num

        # add keys with value == min_val
        keys_with_min = [key for key in key_list
                         if key_track.get(key) == min_val]

        return keys_with_min
