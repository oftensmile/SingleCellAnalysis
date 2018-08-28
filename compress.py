import csv
import numpy as np
import time
from scipy import sparse
from multiprocessing import Pool
import multiprocessing
import os
import util


def get_sparse(filename, start_index, end_index):
    test = []
    period = 1000
    with open(filename, encoding = 'UTF-8') as content:
        for i, line in enumerate(content):
            if(i >= start_index and i < end_index):
                line = line.replace('\n', '').split(',')
                temp = sparse.csr_matrix(line[1:], dtype=float)
                temp.eliminate_zeros()
                test.append(temp)
                if(i % period == 1):
                    test = [sparse.vstack(test)]
            elif(i >= end_index):
                break
    test = sparse.vstack(test)

    return test


def compress_file(fn, save=True):
    filename = fn
    num_lines = sum(1 for line in open(filename, encoding='UTF-8'))
    dvide = multiprocessing.cpu_count()
    length = num_lines // dvide
    index = []
    for i in range(dvide):
        index.append(length * i)
    index.append(num_lines)
    index[0]=1

    p = Pool(dvide)
    res_l =[]
    for i in range(dvide):
        res = p.apply_async(get_sparse, args=(filename, index[i], index[i+1]))
        res_l.append(res)
    p.close()
    p.join()

    x = []
    for i in range(dvide):
        x.append(res_l[i].get())

    data = sparse.vstack(x)
    del res_l
    del x
    if save:    
        sparse.save_npz(filename.split('.')[0] + '.npz',  data.tocsc())
        return filename.split('.')[0] + '.npz'
    else:
        return data.tocsc()


def main():
    fn = util.get_file()
    num = 1
    print('num', num)
    s = time.time()
    l = time.time()
    for _ in range(num):
        compress_file(fn)
        print(time.time() - l)
        l = time.time()
    e = time.time()

    print('average time', (e-s)/num)
    print('total time', e-s)

if __name__ == '__main__':
    main()

