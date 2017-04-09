import shelve
from cachetools import RRCache


class CacheDict:
    """
    Dictionary wrapper that creates a dictionary that
    frequently saves to file but has an in memory
    read cache.
    """

    __slots__ = ['_file_dict', '_cache']

    def __init__(self, name, max_size=2000):
        self._file_dict = shelve.open(name)
        self._cache = RRCache(maxsize=max_size)

    def __getitem__(self, key):
        try:
            # Need the additional step in case of KeyError
            return self._cache[str(key)]
        except KeyError:
            # Need the additional step in case of KeyError
            item = self._file_dict[str(key)]
            self._cache[str(key)] = item
            return item

    def __setitem__(self, key, value):
        self._file_dict[str(key)] = value
        self._cache[str(key)] = value

    def __delitem__(self, key):
        del self._file_dict[str(key)]
        del self._cache[str(key)]

    def __contains__(self, item):
        return item in self._file_dict
