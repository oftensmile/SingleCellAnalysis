#!/usr/bin/env python
import multiprocessing
import os
import time
from multiprocessing import Pool

from scipy import sparse

import util

__author__ = "Razin Shaikh and Minjie Lyu"
__credits__ = ["Razin Shaikh", "Minjie Lyu", "Vladimir Brusic"]
__version__ = "1.0"
__status__ = "Prototype"

def get_data2(content):
    indptr = [0]
    indices = []
    data = []
    for line in content:
        line = line.replace('\n', '').split(',')
        try:
            temp = ([float(i) for i in line[1:]])
        except Exception as _:
            print(line)
            exit(1)

        count = 0
        for i in range(len(temp)):   
            if temp[i] != 0:
                count += 1
                indices.append(i)
                data.append(temp[i])
        indptr.append(indptr[-1] + count)
    return indptr, indices, data


def compress_file(fn):
    data_set = []
    f = open(fn, encoding='UTF-8')
    print(fn)

    content = f.readlines()
    columns_head = content[0].replace('\n', '').split(',')
    content = content[1:]
    shape = [len(content), len(columns_head) - 1]
    
    divide = multiprocessing.cpu_count()
    length = len(content) // divide
    for i in range(divide - 1):
        data_set.append(content[i * length: (i+1) * length])
    data_set.append(content[(i+1) * length: ])
    p = Pool(divide)
    res_l =[]
    for i in range(divide):
        res = p.apply_async(get_data2, args=(data_set[i],))
        res_l.append(res)
    del content
    del data_set
    p.close()
    p.join()

    indptr = [0]
    indices = []
    data = []
    for i in range(divide):
        a, b, c= res_l[i].get()
        indptr.extend([n + indptr[-1] for n in a[1:]])
        indices.extend(b)
        data.extend(c)

    c = sparse.csr_matrix((data, indices, indptr), shape=shape)
    sparse.save_npz('csr_sparse.npz', c)
    coo = c.tocoo()
    sparse.save_npz('coo_sparse.npz', coo)
    csc = c.tocsc()
    sparse.save_npz('csc_sparse.npz', csc)


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
