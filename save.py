import numpy as np
import h5py
from scipy import sparse
import scipy.io
import compress
import row_head
import time
import os
import sys
import util


def save_csv(save_path, data, genes):
    data = data.tocsr()
    with open(save_path + 'csv.csv', 'w') as f:
        for i in range(1, data.shape[1]+1):
            f.write(',%d' % i)
        f.write('\n')
        for i in range(data.shape[0]):
            f.write(genes[i] + ',' + str(data.getrow(i).toarray()[0].tolist())[1:-1].replace(' ', '') + '\n')


def save_mtx(save_path, data, genes, barcodes=None):
    #save mtx
    scipy.io.mmwrite(save_path + 'mtx.mtx', data)

    #save genes
    with open(save_path + 'genes.tsv', 'w') as f:
        for i in genes:
            f.write(i + '\n')

    #save barcodes
    with open(save_path+'barcodes.tsv', 'w') as f:
        if barcodes:
            for i in barcodes:
                f.write(i + '\n')
        else:
            for i in range(1, data.shape[1]+1):
                f.write(str(i) + '\n')


def save_h5(save_path, data, genes, barcodes=None, compression_level=None):
    if not barcodes:
        barcodes = np.array(range(1, data.shape[1]+1), dtype='S')

    with h5py.File(save_path + 'h5.h5', 'w') as hf:
        group = hf.create_group('sct')
        if compression_level:
            group.create_dataset('barcodes', data=barcodes, compression="gzip", compression_opts=compression_level)
            group.create_dataset('gene_names', data=np.array(genes, dtype='S'), compression="gzip", compression_opts=compression_level)
            group.create_dataset('data', data=data.data, compression="gzip", compression_opts=compression_level)
            group.create_dataset('indices', data=data.indices, compression="gzip", compression_opts=compression_level)
            group.create_dataset('indptr', data=data.indptr, compression="gzip", compression_opts=compression_level)
            group.create_dataset('shape', data=data.shape, compression="gzip", compression_opts=compression_level)
        else:
            group.create_dataset('barcodes', data=barcodes)
            group.create_dataset('gene_names', data=np.array(genes, dtype='S'))
            group.create_dataset('data', data=data.data)
            group.create_dataset('indices', data=data.indices)
            group.create_dataset('indptr', data=data.indptr)
            group.create_dataset('shape', data=data.shape)


def save_all(save_path, data, genes):
    s = time.time()
    sparse.save_npz(save_path + 'npz.npz',  data)
    print(time.time() - s)

    s = time.time()
    save_csv(save_path, data, genes)
    print(time.time() - s)

    s = time.time()
    save_mtx(save_path, data, genes)
    print(time.time() - s)

    s = time.time()
    save_h5(save_path, data, genes)
    print(time.time() - s)
