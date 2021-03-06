#!/usr/bin/env python
import time

import numpy as np
import scipy.sparse as sp

import util

__author__ = "Razin Shaikh and Minjie Lyu"
__credits__ = ["Razin Shaikh", "Minjie Lyu", "Vladimir Brusic"]
__version__ = "1.0"
__status__ = "Prototype"

def corr_coef(sp_mat):
    '''Calculates the correlation coefficient of the given matrix
    
    Arguments:
        sp_mat {scipy.sparse} -- The sparse matrix whose correlation coefficient is to be calculated
    
    Returns:
        numpy.array -- The correlation coefficient of the matrix
    '''

    n = sp_mat.shape[1]
    C = ((sp_mat.T*sp_mat -(sum(sp_mat).T*sum(sp_mat)/n))).todense()
    V = np.sqrt(np.mat(np.diag(C)).T*np.mat(np.diag(C)))
    COV = np.divide(C, V + 1e-119)
    del C
    del V
    return COV

def main():
    fn = util.get_file()
    mat = sp.load_npz(fn)
    
    num = 3
    print('num', num)

    s = time.time()
    l = time.time()

    for _ in range(num):
        _ = corr_coef(mat)
        print(time.time() - l)
        l = time.time()
    e = time.time()

    print('average time', (e-s)/num)
    print('total time', e-s)


if __name__ == '__main__':
    main()
