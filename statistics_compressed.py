import time
import numpy as np
from scipy import sparse


def range_num(data, gt = 0, lt = None):
    if(lt):
        val = (data>gt).sum(1) - (data>lt).sum(1)
    else:
        val = (data>gt).sum(1)
    return val

def calculate(fn):
    data = sparse.load_npz(fn)
    shape = data.shape
    row_sum = data.sum(axis = 1)
    row_positive = range_num(data)
    row_max = data.max(axis=1).toarray() # data.max returns a sparse matrix
    col_sum = data.sum(axis = 0)
    col_positive = (data != 0).sum(0)
    col_max = data.max(axis = 0)

    #TODO: Get the number of zeros for each column

    typical = []
    typical.append(range_num(data, 0, 1))
    typical.append(range_num(data, 1, 2))
    typical.append(range_num(data, 2, 4))
    typical.append(range_num(data, 4, 8))
    typical.append(range_num(data, 8, 16))
    typical.append(range_num(data, 16, 32))
    typical.append(range_num(data, 32, 64))
    typical.append(range_num(data, 64, 128))
    typical.append(range_num(data, 128, 256))
    typical.append(range_num(data, 256, 512))
    typical.append(range_num(data, 512, 1024))
    typical.append(range_num(data, 1024, 2048))
    typical.append(range_num(data, 2048, 4096))
    typical.append(range_num(data, 4096, 8192))
    typical.append(range_num(data, 8192))

    row_median = []
    for i, m in enumerate(((data != 0).sum(1) > shape[1]//2).tolist(), 0):
        if m[0]:
            temp = data.getrow(i).toarray().reshape(data.shape[1],)
            row_median.append(np.median(temp))
        else:
            row_median.append(0)


def main():
    num = 10
    print('num', num)
    s = time.time()
    l = time.time()
    for _ in range(num):
        calculate('csc_sparse.npz')
        print(time.time() - l)
        l = time.time()
    e = time.time()

    print('average time', (e-s)/num)
    print('total time', e-s)

if __name__ == '__main__':
    main()