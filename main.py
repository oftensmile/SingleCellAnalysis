import os
import sys

import h5py
import scipy.io
from scipy import sparse as sp

import compress
import convert
import filter_data
import row_head
import save
import util

GENE_TO_ENSG = 'hg19_hg38.csv'
ENSG_TO_GENE = 'convert_mapping.csv'


def get_matrix_and_genes(filename):
    ext = os.path.splitext(filename)[1]
    if ext == '.h5':
        tmp = filename.get(list(filename.keys())[0])
        matrix = sp.csc_matrix((tmp['data'][()], tmp['indices'][()], tmp['indptr'][()]), shape=tuple(tmp['shape'][()]))
        genes_tmp = list(map(lambda x: x.decode('utf-8'), list(tmp['barcodes'])))
    elif ext == '.csv':
        matrix = compress.compress_file(filename, save=False)
        genes_tmp = row_head.return_row_head(filename)
    elif ext == '.mtx':
        gene_file = util.get_file('Select genes')
        with open(gene_file) as gen:
            tmp = gen.readlines()
            genes_tmp = list(map(lambda x: x.replace('\n', ''), tmp))
        matrix = scipy.io.mmread(filename)
    else:
        sys.exit("Unsupported file type")
    
    genes = []

    if "ENSG" in genes_tmp[0]:
        if len(genes_tmp[0]) != 15:
            if genes_tmp[0].index("ENSG") == 0:
                genes = list(map(lambda x: x[:15], genes_tmp))
            else:
                genes = list(map(lambda x: x[-15:], genes_tmp))
        else:
            genes = genes_tmp
    else:
        genes = genes_to_ensg(genes_tmp)

    return matrix, genes


def genes_to_ensg(genes):
    try:
        f = open(GENE_TO_ENSG)
    except FileNotFoundError as _:
        f = util.get_file("Select mappings file")
    
    m = list(map(lambda x : x.replace('\n', '').split(','), f.readlines()))

    from_map = [line[1] for line in m]
    to_map = [line[0] for line in m]

    ensg = []

    for gene in genes:
        try:
            ensg.append(to_map[from_map.index(gene)])
        except ValueError as _:
            ensg.append(gene)

    f.close()

    return ensg


def main():
    filename = util.get_file("Select the file")

    save_path = os.path.join(os.path.dirname(os.path.abspath(filename)), os.path.splitext(os.path.split(filename)[1])[0])

    threshold = util.prompt_integer("Enter integer", "Select threshold for filtering (0 for no filtering)")
    matrix, genes = get_matrix_and_genes(filename)

    with open(ENSG_TO_GENE) as f:
        mappings = f.readlines()
        matrix, genes = convert.standardize(genes, matrix, mappings)

    if threshold != 0:
        matrix = filter_data.filter_data(matrix, threshold)

    save.save_all(save_path, matrix, genes)

if __name__ == '__main__':
    main()
