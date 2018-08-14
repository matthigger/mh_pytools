def grouped(iterable, n):
    """ http://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list 
    """
    return zip(*[iter(iterable)] * n)