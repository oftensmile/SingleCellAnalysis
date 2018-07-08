import numpy as np
import scipy.sparse as sp
import time
import util

def corr_coef(sp_mat):
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