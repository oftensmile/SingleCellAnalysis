#!/usr/bin/env python
import h5py
import numpy as np
import scipy.io
from scipy import sparse

__author__ = "Razin Shaikh and Minjie Lyu"
__credits__ = ["Razin Shaikh", "Minjie Lyu", "Vladimir Brusic"]
__version__ = "1.0"
__status__ = "Prototype"

def save_csv(save_path, data, genes):
    data = data.tocsr()
    with open(save_path + '_csv.csv', 'w') as f:
        for i in range(1, data.shape[1]+1):
            f.write(',%d' % i)
        f.write('\n')
        for i in range(data.shape[0]):
            f.write(genes[i] + ',' + str(data.getrow(i).toarray()[0].tolist())[1:-1].replace(' ', '') + '\n')


def save_mtx(save_path, data, genes, barcodes=None):
    #save mtx
    scipy.io.mmwrite(save_path + '_mtx.mtx', data)

    #save genes
    with open(save_path + '_genes.tsv', 'w') as f:
        for i in genes:
            f.write(i + '\n')

    #save barcodes
    with open(save_path+'_barcodes.tsv', 'w') as f:
        if barcodes:
            for i in barcodes:
                f.write(i + '\n')
        else:
            for i in range(1, data.shape[1]+1):
                f.write(str(i) + '\n')


def save_h5(save_path, data, genes, barcodes=None, compression_level=4):
    if not barcodes:
        barcodes = np.array(range(1, data.shape[1]+1), dtype='S')

    with h5py.File(save_path + '_h5.h5', 'w') as hf:
        group = hf.create_group('sct')
        if compression_level:
            group.create_dataset('barcodes', data=barcodes, compression="gzip", compression_opts=compression_level)
            group.create_dataset('gene_names', data=np.array(genes, dtype='S'), compression="gzip", compression_opts=compression_level)
            group.create_dataset('data', data=data.data, compression="gzip", compression_opts=compression_level)
            group.create_dataset('indices', data=data.indices, compression="gzip", compression_opts=compression_level)
            group.create_dataset('indptr', data=data.indptr, compression="gzip", compression_opts=compression_level)
            group.create_dataset('shape', data=data.shape, compression="gzip", compression_opts=compression_level)


def save_all(save_path, data, genes):
    sparse.save_npz(save_path + '_npz.npz',  data)
    save_csv(save_path, data, genes)
    save_mtx(save_path, data, genes)
    save_h5(save_path, data, genes)
