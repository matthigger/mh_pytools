import weakref


def flyfactory(weak=False):
    """ returns a FlyWeight superclass

    https://en.wikipedia.org/wiki/Flyweight_pattern

    we build many unique flyweight superclasses so that their instances do not
    intersect each other

    Args:
         weak (bool): toggles weakref, if True allows obj in dict to be garbage
                      collected

    Returns:
        FlyWeight: FlyWeight class
    """

    class FlyWeight:
        """ superclass, makes an object fit flyweight pattern
        """

        if weak:
            raise NotImplementedError
            instances = weakref.WeakValueDictionary()
        else:
            instances = dict()

        @classmethod
        def factory(cls, *args, **kwargs):
            """ alternative to __init__ which utilizes flyweight

            if the subclass has an init_hash fnc it is used to determine if the
            obj has already been created.  init_hash is a fnc which accepts
            same parameters as subcls.__init__, returns some hashable key which
            is associated with the creation of that obj

            if no init_hash is implemented then the obj is assumed hashable
            itself and is its own key.  (consider using init_hash to avoid
            expensive calls to subclass.__init__)
            """
            if hasattr(cls, 'init_hash'):
                h = cls.init_hash(*args, **kwargs)
                if h in cls.instances.keys():
                    # todo: what if obj was garbage collected?
                    return cls.instances[h]

            # build new obj
            obj = cls.__new__(cls)
            obj.__init__(*args, **kwargs)

            if not hasattr(cls, 'init_hash'):
                h = obj

            # find obj + return its copy (seen before).
            # otherwise, set and return the obj (not seen before)
            return cls.instances.setdefault(h, obj)

    return FlyWeight


if __name__ == '__main__':
    from pprint import pprint
    import doctest


    class Spam(flyfactory(weak=False)):
        """
        >>> x = Spam.factory(1)
        new obj created: 1
        >>> y = Spam.factory(1)
        >>> # note: new obj not created (__init__ never called)
        >>> x is y
        True
        >>> much_spam = [Spam.factory(idx) for idx in range(4)]
        new obj created: 0
        new obj created: 2
        new obj created: 3
        >>> pprint(dict(Spam.instances))
        {0: Spam(0), 1: Spam(1), 2: Spam(2), 3: Spam(3)}
        """

        def __init__(self, a):
            self.a = a
            print(f'new obj created: {a}')

        def __repr__(self):
            return f'Spam({self.a})'

        @staticmethod
        def init_hash(a):
            return a


    doctest.testmod()
