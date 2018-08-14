import gzip
import pickle

import nrrd


def get_open(file):
    file = str(file)

    if file.endswith('.nhdr') or file.endswith('.nrrd'):
        fnc_open = nrrd.read
    elif file.endswith('.p.gz'):
        fnc_open = gzip.open
    else:
        fnc_open = open

    return fnc_open


def load(file):
    """ gets whatever is in the file (zippped or not) """
    file = str(file)
    fnc_open = get_open(file)

    if fnc_open == nrrd.read:
        x, nrrd_dict = nrrd.read(file)
        return x, nrrd_dict

    with fnc_open(file, 'rb') as f:
        out = pickle.load(f)

    return out


def save(to_save, file):
    fnc_open = get_open(file)

    with fnc_open(file, 'wb') as f:
        pickle.dump(to_save, f)
