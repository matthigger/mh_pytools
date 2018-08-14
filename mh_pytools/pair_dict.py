class PairDict(dict):
    """ enforces pair_dict[a, b] = pair_dict[b, a] by only storing value once

    >>> p = PairDict()
    >>> p[('a', 'b')] = 1
    >>> p[('c', 'b')] = 2
    >>> p[('b', 'c')]
    2
    """

    @staticmethod
    def from_dict(d):
        c = PairDict()
        c.update(d)
        return c

    def __getitem__(self, key):
        return super().__getitem__(frozenset(k for k in key))

    def __setitem__(self, key, value):
        super().__setitem__(frozenset(k for k in key), value)
