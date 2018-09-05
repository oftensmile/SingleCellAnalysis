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

ENSG_TO_GENE = 'convert_mapping.csv'

def get_matrix_and_genes(filename):
    '''Read the given file and extract the data matrix (scipy sparse) and the list of genes in ENSG.
    
    Arguments:
        filename {string} -- The path of file. Supported file types are H5, CSV and MTX
    
    Returns:
        scipy.sparse.csc_matrix -- sparse data matrix 
        list -- genes list in ENSG
    '''

    ext = os.path.splitext(filename)[1]
    if ext == '.h5':
        tmp = filename.get(list(filename.keys())[0])
        matrix = sp.csc_matrix((tmp['data'][()], tmp['indices'][()], tmp['indptr'][()]), shape=tuple(tmp['shape'][()]))
        genes = list(map(lambda x: x.decode('utf-8'), list(tmp['barcodes'])))
    elif ext == '.csv':
        matrix = compress.compress_file(filename, save=False)
        genes = row_head.return_row_head(filename)
    elif ext == '.mtx':
        gene_file = util.get_file('Select genes')
        with open(gene_file) as gen:
            tmp = gen.readlines()
            genes = list(map(lambda x: x.replace('\n', ''), tmp))
        matrix = scipy.io.mmread(filename)
    else:
        sys.exit("Unsupported file type")

    return matrix, genes


def main():
    '''
    * Get file
    * Get threshold for filtering
    * Get the matrix and genes from the file
    * Standarized the matrix and genes (ENSG)
    * Filter, if needed
    * Save in CSV, H5 and MEX(mtx, tsv)
    '''

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
