import copy

import numpy as np
import math


class Tree(dict):
    """
    >>> t = Tree(3)
    >>> t[0][1][5] = 'hello'
    >>> t[0][4] = 'hello again'
    >>> for k, v in t:
    ...     print('{}: {}'.format(k, v))
    (0, 1, 5): hello
    (0, 4): hello again
    >>> t[0][1][2][3] = 'is this too much?'
    Traceback (most recent call last):
    ...
    IndexError: tree has no more levels
    >>> a = Tree()
    >>> a[0][1][5] = 'hello (overwrite)'
    >>> a[0][1][1] = 'a whole new node'
    >>> t.add(a, overwrite=False, in_place=False)
    Traceback (most recent call last):
    ...
    KeyError: 'overwrite error: node already present'
    >>> ta = t.add(a, overwrite=True, in_place=True)
    >>> for k, v in ta:
    ...     print('{}: {}'.format(k, v))
    (0, 1, 1): a whole new node
    (0, 1, 5): hello (overwrite)
    (0, 4): hello again
    >>> for k, v in ta.__iter__(n_level=2):
    ...     print('{}: {}'.format(k ,v))
    (0, 1): {1: 'a whole new node', 5: 'hello (overwrite)'}
    (0, 4): hello again
    """

    def __init__(self, *args, n_levels=np.inf, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_levels = n_levels

    def __getitem__(self, item):
        if item in self.keys():
            # item found, return it
            return super().__getitem__(item)
        elif self.n_levels > 1:
            # item not found, init to a tree with one fewer levels, return that
            self[item] = Tree(n_levels=self.n_levels - 1)
            return self[item]
        else:
            # not enough levels left
            raise IndexError('tree has no more levels')

    def __iter__(self, prev_keys=[], n_level=np.inf):
        n_level -= 1
        for k, v in self.items():
            _prev_keys = prev_keys + [k]
            if isinstance(v, Tree) and n_level:
                # return key value pairs recursively for Tree self[k]
                for _k, _v in self[k].__iter__(prev_keys=_prev_keys,
                                               n_level=n_level):
                    yield _k, _v
            else:
                # return key value pairs
                yield tuple(_prev_keys), v

    def set_by_tuple(self, key_tuple, val, overwrite=True, root=None):
        if root is None:
            root = self

        if len(key_tuple) == 1:
            if not overwrite and key_tuple[0] in root.keys():
                raise KeyError('overwrite error: node already present')
            root[key_tuple[0]] = val
            return

        if key_tuple[0] in root.keys():
            if not isinstance(root[key_tuple[0]], Tree):
                raise AttributeError('current tree leaf must stay leaf')
        else:
            # access below initializes it via __getitem__
            root[key_tuple[0]]

        # progress down tree
        self.set_by_tuple(tuple(key_tuple[1:]), val, overwrite=overwrite,
                          root=root[key_tuple[0]])

    def add(self, other, overwrite=False, in_place=True):
        if in_place:
            tree_out = self
        else:
            tree_out = copy.deepcopy(self)

        for key_tuple, val in other:
            tree_out.set_by_tuple(key_tuple, val, overwrite=overwrite)
        return tree_out
