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


def main(mtx):
    
    save_path = os.path.join(os.path.dirname(os.path.abspath(mtx)), 'convert', os.path.splitext(os.path.split(mtx)[1])[0][:-3])

    mat = scipy.io.mmread(mtx)
    spr = filter_data(mat, 100)
    if spr.shape[0] == 32738:
        gene_tsv = 'hg19.csv'
    elif spr.shape[0] == 32738:
        gene_tsv = 'hg38.csv'
    else:
        print('ERROR************')
        exit(1)
    with open(gene_tsv) as g:
        genes = list(map(lambda x: x.replace('\n', ''), g.readlines()))

    new_genes, new_data = nc.standardize(genes, spr)
    nc.save_all(save_path, new_data, new_genes)




if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("usage: " + sys.argv[0] + " MTX_FILE.mtx GENE_NAMES.tsv")
        sys.exit(1)
    main('062_3K_human_PBMC_healthy_mtx.mtx')
