#!/usr/bin/env python
import multiprocessing
import os
import time
from multiprocessing import Pool

import numpy as np
from scipy import sparse

import util

__author__ = "Razin Shaikh and Minjie Lyu"
__credits__ = ["Razin Shaikh", "Minjie Lyu", "Vladimir Brusic"]
__version__ = "1.0"
__status__ = "Prototype"

def get_sparse(filename, start_index, end_index):
    '''Generates the sparse matrix from the CSV file in the range of line start_index to line end_index-1 
    
    Arguments:
        filename {string} -- Path of CSV file
        start_index {int} -- The starting line number from CSV file for sparse matrix
        end_index {int} -- The (last line number + 1) from CSV file for sparse matrix
    
    Returns:
        scipy.sparse.csr_matrix -- The compressed sparse matrix generated from data read from CSV file
    '''

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
    '''Compresses a CSV file to scipy.sparse matrix
    
    Arguments:
        fn {string} -- Path of CSV file
    
    Keyword Arguments:
        save {bool} -- Determines whether the file should be saved to disk (.npz file) (default: {True})
    
    Returns:
        [string, scipy.sparse.csr_matrix] -- Return the path of saved file if save=True, 
                                             else returns the compressed scipy.sparse csr matrix.
    ''' 
    
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
