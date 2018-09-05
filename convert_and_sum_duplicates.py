import util
import time
import convert_mappings
import compress
import row_head
import convert_sparse_to_csv
import scipy
from scipy import sparse
import numpy as np
from collections import defaultdict

'''This file is depricated. Do not use.'''

def main():
    input_file = util.get_file("Select the file to be converted")
    mappings = util.get_file("Select the mapping")

    s = time.time()

    convert_mappings.convert_mappings(input_file, mappings)

    npz_file = compress.compress_file(''.join(input_file.split('.')[:-1]) + '_converted.' + input_file.split('.')[-1])
    rh_file = row_head.save_row_head(''.join(input_file.split('.')[:-1]) + '_converted.' + input_file.split('.')[-1])

    with open(rh_file) as h:
        row_heads = list(map(lambda x: x.replace('\n', ''), h.readlines()))

    mat = sparse.load_npz(npz_file).tocsr()

    rows_delete = []
    for gene, dup in list_duplicates(row_heads):
        print(gene, dup)
        set_row_csr(mat, dup[0], sum(mat.getrow(x) for x in dup).toarray()[0])
        rows_delete.extend(dup[1:])
        
    mat.eliminate_zeros()
        
    for i in sorted(rows_delete, reverse=True):
        delete_row_csr(mat, i)
        row_heads.pop(i)

    dup_row = rh_file.split('.')[0] + '_dup.txt'
    dup_npz = npz_file.split('.')[0] + '_dup.npz'

    with open(dup_row, 'w') as h:
        h.write(str(row_heads)[1:-1].replace('\'', '').replace(', ', '\n'))

    sparse.save_npz(dup_npz, mat)

    spr, rh, _, output_file = convert_sparse_to_csv.get_data_from_files(dup_npz, dup_row, isMtx=False)
    convert_sparse_to_csv.sparse_to_csv(spr, rh, output_file)

    print(time.time() - s)


def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)


#https://stackoverflow.com/questions/28427236/set-row-of-csr-matrix
def set_row_csr(A, row_idx, new_row):
    assert sparse.isspmatrix_csr(A), 'A shall be a csr_matrix'
    assert row_idx < A.shape[0], 'The row index ({0}) shall be smaller than the number of rows in A ({1})'.format(row_idx, A.shape[0])
    try:
        N_elements_new_row = len(new_row)
    except TypeError:
        msg = 'Argument new_row shall be a list or numpy array, is now a {0}'        .format(type(new_row))
        raise AssertionError(msg)
    N_cols = A.shape[1]
    assert N_cols == N_elements_new_row, 'The number of elements in new row ({0}) must be equal to ' 'the number of columns in matrix A ({1})'             .format(N_elements_new_row, N_cols)

    idx_start_row = A.indptr[row_idx]
    idx_end_row = A.indptr[row_idx + 1]
    additional_nnz = N_cols - (idx_end_row - idx_start_row)

    A.data = np.r_[A.data[:idx_start_row], new_row, A.data[idx_end_row:]]
    A.indices = np.r_[A.indices[:idx_start_row], np.arange(N_cols), A.indices[idx_end_row:]]
    A.indptr = np.r_[A.indptr[:row_idx + 1], A.indptr[(row_idx + 1):] + additional_nnz]


#https://stackoverflow.com/questions/13077527/is-there-a-numpy-delete-equivalent-for-sparse-matrices
def delete_row_csr(mat, i):
    if not isinstance(mat, scipy.sparse.csr_matrix):
        raise ValueError("works only for CSR format -- use .tocsr() first")
    n = mat.indptr[i+1] - mat.indptr[i]
    if n > 0:
        mat.data[mat.indptr[i]:-n] = mat.data[mat.indptr[i+1]:]
        mat.data = mat.data[:-n]
        mat.indices[mat.indptr[i]:-n] = mat.indices[mat.indptr[i+1]:]
        mat.indices = mat.indices[:-n]
    mat.indptr[i:-1] = mat.indptr[i+1:]
    mat.indptr[i:] -= n
    mat.indptr = mat.indptr[:-1]
    mat._shape = (mat._shape[0]-1, mat._shape[1])


if __name__ == '__main__':
    main()