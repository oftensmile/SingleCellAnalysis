import numpy as np
from scipy import sparse as sp

def filter_data(mat, threshold):
    '''Select the columns in the matrix where the number of positives is greater than the threshold.
    
    Arguments:
        mat {scipy.sparse} -- The matrix that is to be filtered
        threshold {int} -- The threshold for filtering
    
    Returns:
        scipy.sparse.csc_matrix -- The filtered matrix
    '''

    mat = mat.tocsc()
    sumcol = np.squeeze(np.array((mat>0).sum(axis=0)))
    columns, = np.where(sumcol > threshold)

    cols = []
    for i in columns:
        cols.append(mat.getcol(i))

    filtered = sp.hstack(cols)

    return filtered
