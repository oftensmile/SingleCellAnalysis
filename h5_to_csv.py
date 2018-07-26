import numpy as np
from scipy.sparse import csr_matrix, csc_matrix
import h5py
import convert_sparse_to_csv
import util

def get_list(l):
    return list(map(lambda x: x.decode('utf-8'), list()))


def h5_to_csv(input_file):
    f = h5py.File('GSM2888372_8h.h5')
    output_file = str(input_file.split('.')[:-1])[2:-2]

    d = f.get(list(f.keys())[0])

    spr = csc_matrix((d['data'][()], d['indices'][()], d['indptr'][()]), shape=tuple(d['shape'][()]))

    convert_sparse_to_csv.split_and_convert(spr, get_list(d['gene_names']), get_list(d['barcodes']), output_file)


def main():
    input_file = util.get_file('Select h5 file')
    h5_to_csv(input_file)

if __name__ == '__main__':
    main()