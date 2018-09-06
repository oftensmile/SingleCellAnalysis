#!/usr/bin/env python
import time
from multiprocessing import Pool

import numpy as np
from scipy import sparse

__author__ = "Razin Shaikh and Minjie Lyu"
__credits__ = ["Razin Shaikh", "Minjie Lyu", "Vladimir Brusic"]
__version__ = "1.0"
__status__ = "Prototype"

def get_data(content):
    data = []
    for i in content:
        data.append(change(i))
    data = np.array(data)
    row_sum = np.sum(data, axis=1)
    row_positive = np.count_nonzero(data,axis=1)
    row_max = np.max(data, axis=1)
    row_median = np.median(data, axis=1)
    return  row_sum, row_positive, row_max, row_median, data


def change(x):
    if x[-1] != '\n':
        return np.fromstring(x[x.index(',')+1:], dtype=float, sep=',')
    else:
        return  np.fromstring(x[x.index(',')+1:-1], dtype=float, sep=',')


def functionDemo():
    start = time.time()
    data_set = []
    f = open('015-Frozen_PBMCs_DonorB genes 7783.csv')

    content = f.readlines()
    columns_head = content[0].replace('\n', '').split(',')
    content = content[1:]
    shape = [len(content), len(columns_head) - 1]
    

    divide = 4
    length = len(content) // divide
    modnum = len(content) % divide
    
    index = 0
    for i in range(divide):
        data_set.append(content[index: index + length])
        index += length

    p = Pool(divide)
    res_l =[]
    for i in range(divide):
        res = p.apply_async(get_data, args=(data_set[i],))
        # print(i)
        res_l.append(res)
    p.close()
    p.join()

    data = np.array([])
    row_sum = np.array([])
    row_positive = np.array([])
    row_max = np.array([])
    row_median = np.array([])
    
    for i in range(divide):
        a, b, c, d, e= res_l[i].get()
        row_sum = np.append(row_sum, a)
        row_positive = np.append(row_positive, b)
        row_max = np.append(row_max, c)
        row_median = np.append(row_median, d)
        data = np.append(data, e)

    data = data.reshape(index, shape[1])
    col_sum = np.sum(data, axis=0)
    col_positive = np.count_nonzero(data, axis=0)
    col_max = np.max(data, axis =0)
    print(time.time() - start)
    

def main():
    num = 10
    print('num', num)
    s = time.time()
    l = time.time()
    for _ in range(num):
        functionDemo()
        print(time.time() - l)
        l = time.time()
    e = time.time()

    print('average time', (e-s)/num)
    print('total time', e-s)

if __name__ == '__main__':
    main()
