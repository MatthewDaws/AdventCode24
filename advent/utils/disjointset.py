class DisjointSet:
    def __init__(self, iterable=None):
        self._elements = dict()
        if iterable is not None:
            for x in iterable:
                self.add(x)
        
    @property
    def entries(self):
        """Returns set of elements"""
        return set(self._elements.keys())
    
    def contains(self, element):
        """Does the disjoint set currently contain `element`?"""
        return element in self._elements

    def as_sets(self):
        lookup = dict()
        for key in self._elements.keys():
            root = self._find_entry(key)
            if root not in lookup:
                lookup[root] = set()
            lookup[root].add(key)
        return {frozenset(x) for x in lookup.values()}

    def add(self, element):
        """Add a (possibly) new `element`."""
        if element in self._elements:
            return
        self._elements[element] = DisjointSet.Entry()

    def find(self, element):
        """Find an abstract representative of the partition containing `element`, else raises `KeyError`"""
        return hash(self._find_entry(element))

    def _find_entry(self, element):
        entry = self._elements[element]
        while entry.parent is not None:
            entry = entry.parent
        return entry

    def find_depth(self):
        maxdepth = 0
        for entry in self._elements.values():
            depth = 0
            while entry.parent is not None:
                entry = entry.parent
                depth += 1
            maxdepth = max(maxdepth, depth)
        return maxdepth

    def union(self, a, b):
        """Merge the partitions containing elements `a` and `b`; raises `KeyError` if these elements are not present."""
        aentry = self._find_entry(a)
        bentry = self._find_entry(b)
        if aentry is bentry:
            return
        if aentry.rank < bentry.rank:
            aentry, bentry = bentry, aentry
        bentry.parent = aentry
        if aentry.rank == bentry.rank:
            aentry.rank += 1

    class Entry:
        def __init__(self):
            self.parent = None
            self.rank = 0
