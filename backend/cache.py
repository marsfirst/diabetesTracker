"""
backend.cache

Simple LRUCache implementation for demo and educational purposes.
"""
from collections import OrderedDict

class LRUCache:
    """A small LRU cache using OrderedDict.

    Methods:
    - get(key): returns value or None
    - put(key, value): insert/update
    - items(): list of (key, value) from least->most recent
    - stats(): dict with capacity, size, hits, misses
    """
    def __init__(self, capacity=5):
        self.capacity = int(capacity)
        self._data = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self._data:
            self.hits += 1
            value = self._data.pop(key)
            self._data[key] = value
            return value
        self.misses += 1
        return None

    def put(self, key, value):
        if key in self._data:
            self._data.pop(key)
        elif len(self._data) >= self.capacity:
            self._data.popitem(last=False)  # pop least recently used
        self._data[key] = value

    def items(self):
        return list(self._data.items())

    def stats(self):
        return {
            'capacity': self.capacity,
            'size': len(self._data),
            'hits': self.hits,
            'misses': self.misses,
        }

if __name__ == '__main__':
    # Quick manual test
    c = LRUCache(3)
    c.put(1, 'A')
    c.put(2, 'B')
    c.put(3, 'C')
    print('Items:', c.items())
    c.get(2)
    c.put(4, 'D')
    print('After adding 4 (evict 1):', c.items(), 'stats', c.stats())
