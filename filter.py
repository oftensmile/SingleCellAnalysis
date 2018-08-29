import os
import sys

import numpy as np
import scipy.io
from scipy import sparse as sp

import new_convert as nc


def filter_data(mat, threshold):
    mat = mat.tocsc()
    sumcol = np.squeeze(np.array(mat.sum(axis=0)))
    columns, = np.where(sumcol > threshold)

    cols = []
    for i in columns:
        cols.append(mat.getcol(i))

    filtered = sp.hstack(cols)

    return filtered


def main(mtx, gene_tsv):
    
    save_path = os.path.join(os.path.dirname(os.path.abspath(mtx)), 'convert', os.path.splitext(os.path.split(mtx)[1])[0][:-3])

    mat = scipy.io.mmread(mtx)
    spr = filter_data(mat, 100)

    with open(gene_tsv) as g:
        genes = list(map(lambda x: x.replace('\n', ''), g.readlines()))

    new_genes, new_data = nc.standardize(genes, spr)
    nc.save_all(save_path, new_data, new_genes)




if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: " + sys.argv[0] + " MTX_FILE.mtx GENE_NAMES.tsv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
