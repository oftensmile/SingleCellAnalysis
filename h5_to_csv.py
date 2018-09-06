#!/usr/bin/env python
import h5py
import numpy as np
from scipy.sparse import csc_matrix, csr_matrix

import convert_sparse_to_csv
import util

__author__ = "Razin Shaikh and Minjie Lyu"
__credits__ = ["Razin Shaikh", "Minjie Lyu", "Vladimir Brusic"]
__version__ = "1.0"
__status__ = "Prototype"

def get_list(l):
    return list(map(lambda x: x.decode('utf-8'), list(l)))


def h5_to_csv(input_file):
    f = h5py.File(input_file)
    output_file = str(input_file.split('.')[:-1])[2:-2]

    d = f.get(list(f.keys())[0])

    spr = csc_matrix((d['data'][()], d['indices'][()], d['indptr'][()]), shape=tuple(d['shape'][()]))

    row_heads = get_list(d['gene_names'])
    convert_sparse_to_csv.sparse_to_csv(spr, row_heads, output_file)


def main():
    input_file = util.get_file('Select h5 file')
    h5_to_csv(input_file)

if __name__ == '__main__':
    main()
