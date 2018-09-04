import numpy as np
from scipy.sparse import csr_matrix, csc_matrix
import h5py
import convert_sparse_to_csv
import util

def get_list(l):
    return list(map(lambda x: x.decode('utf-8'), list(l)))


def h5_to_csv(input_file):
    f = h5py.File(input_file)
    output_file = str(input_file.split('.')[:-1])[2:-2]

    d = f.get(list(f.keys())[0])

    spr = csc_matrix((d['data'][()], d['indices'][()], d['indptr'][()]), shape=tuple(d['shape'][()]))

    row_heads = get_list(d['gene_names'])
    barcodes = get_list(d['barcodes'])
    # convert_sparse_to_csv.split_and_convert(spr, row_heads, barcodes, output_file)
    convert_sparse_to_csv.sparse_to_csv(spr, row_heads, output_file)


def main():
    input_file = util.get_file('Select h5 file')
    h5_to_csv(input_file)

if __name__ == '__main__':
    main()