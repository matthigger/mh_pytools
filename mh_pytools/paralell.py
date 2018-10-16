import gc
import multiprocessing

from tqdm import tqdm


def add_one(x):
    """ dummy for test"""
    return x + 1


class AddState:
    """ dummy for test"""

    def __init__(self, state):
        self.state = state

    def add_state(self, x):
        return self.state + x


def proxy_fnc(dict_in):
    """
    >>> proxy_fnc(fnc=add_one, x=1)
    2
    """
    # get fnc, rm from dict_in
    fnc = dict_in['fnc']
    del dict_in['fnc']

    # apply fnc to unpacked dict_in
    return fnc(**dict_in)


def proxy_fnc_obj(fnc_name, obj, **kwargs):
    fnc = getattr(obj, fnc_name)
    return fnc(**kwargs)


def join(pool, res, check_sec=1, verbose=True, desc='task', garbage=True):
    """ counts progress in a set of multiprocessing.async result objects

    Args:
        pool (multiprocessing.Pool):
        res: results obj, output of pool.map_async() and similar
        check_sec (float): time between checks
        verbose (bool): whether to print to command line
        desc (str): what to print to command line
        garbage (bool): whether to run garbage collection when task is done

    Returns:
        res.get()
    """
    pool.close()

    left = res._number_left
    pbar = tqdm(total=left, disable=(not verbose), desc=desc)

    if garbage:
        gc.enable()

    while not res.ready():
        delta = left - res._number_left
        left -= delta
        if delta:
            pbar.update(delta)
        res.wait(check_sec)
    pbar.update(left)

    pool.join()

    if garbage:
        gc.collect()

    return res.get()


def run_par_fnc(fnc, arg_list, desc=None, **kwargs):
    """ runs a function in parallel

    Args:
        fnc (fnc or str): function to be run in paralell, or name of method to
                          be run in parallel
        arg_list (list): list of dicts, to be unpacked in running fnc
        desc (str): description of operation

    Returns:
        res_list (list): list of results, same order as arg_list

    >>> run_par_fnc(add_one, [{'x': x} for x in range(10)], verbose=False)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """

    if desc is None:
        desc = fnc.__name__

    for d in arg_list:
        d['fnc'] = fnc

    pool = multiprocessing.Pool()
    res = pool.map_async(proxy_fnc, arg_list)
    return join(pool, res, desc=desc, **kwargs)