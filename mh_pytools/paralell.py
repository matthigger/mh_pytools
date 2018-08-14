import gc
import multiprocessing.pool
import time
from itertools import islice

import multiprocess
from tqdm import tqdm


def take_dict(fnc):
    def fnc_dict(d):
        return fnc(**d)

    return fnc_dict


def iter_dict(dict_in, num_part):
    """ partitions a dict into a iterator of dicts

    >>> d = {k: k for k in range(10)}
    >>> list(iter_dict_partition(d, 3))
    [{0: 0, 1: 1, 2: 2, 3: 3}, {4: 4, 5: 5, 6: 6}, {8: 8, 9: 9, 7: 7}]
    """
    size = int(len(dict_in) / num_part)
    num_extra = len(dict_in) % num_part

    it = iter(dict_in.items())
    for i in range(num_part):
        yield dict(islice(it, size + (i < num_extra)))


def join(pool, res, *args, **kwargs):
    if isinstance(res, multiprocessing.pool.MapResult) or \
            isinstance(res, multiprocess.pool.MapResult):
        return join_map(pool, res, *args, **kwargs)
    else:
        raise NotImplementedError('wait_update_iter needs revision')
        return join_iter(pool, res, *args, **kwargs)


def join_map(pool, res, check_sec=1, verbose=True, desc='task', garbage=True):
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


def join_iter(result_iter, check_sec=1, verbose=True, desc='task',
              del_res_set=False, garbage=True):
    """ counts progress in a set of multiprocessing.async result objects

    Args:
        result_iter (iter): multiprocessing.async result objects
        check_sec (float): time between checks
        verbose (bool): whether to print to command line
        desc (str): what to print to command line
        del_res_set (bool): if true then the result_iter (required as set) is d
                            destroyed by wait_update.  This is helpful as once
                            a task is completed any refs to results are
                            destroyed which frees up memory
        garbage (bool): whether to run garbage collection when task is done
    """
    pbar = tqdm(total=len(result_iter), disable=(not verbose), desc=desc)

    if del_res_set:
        if not isinstance(result_iter, set):
            raise AttributeError('passed result_iter which is not set')
        res_set = result_iter
    else:
        res_set = set(result_iter)

    if garbage:
        gc.enable()

    while res_set:
        # check if any tasks are done
        res_done = next((x for x in res_set if x.ready()), None)
        if res_done is None:
            time.sleep(check_sec)
            continue

        # if task is done, update progress bar
        res_set.remove(res_done)
        pbar.update(1)

        if garbage:
            gc.collect()
