#!/usr/bin/env python
import os

import numpy as np
import scipy.io
from scipy import sparse

import compress
import util

__author__ = "Razin Shaikh and Minjie Lyu"
__credits__ = ["Razin Shaikh", "Minjie Lyu", "Vladimir Brusic"]
__version__ = "1.0"
__status__ = "Prototype"

def range_num_row(data, gt = 0, lt = None):
    if(lt):
        val = (data>gt).sum(1) - (data>lt).sum(1)
    else:
        val = (data>gt).sum(1)
    return val

def range_num(list_data, gt, lt = None):
    if(lt):
        val = (list_data>gt).sum() - (list_data>lt).sum()
    else:
        val = (list_data == gt).sum()
    return val



def calculate(fn, data):
    data = data.tocsr()
    shape = data.shape
    col_min = data.min(axis=0).toarray().reshape(shape[1])
    col_max = data.max(axis=0).toarray().reshape(shape[1])
    col_positive = np.array((data != 0).sum(0)).reshape(shape[1])
    col_median = []
    for i, m in enumerate((np.array((data != 0).sum(0) > shape[0]//2)).reshape(shape[1]), 0):
        if m:
            temp = data.getcol(i).toarray().reshape(data.shape[0],)
            col_median.append(np.median(temp))
        else:
            col_median.append(0)

    col_median = np.array(col_median)
    temp_1 = np.copy(col_min)
    temp_2 = np.copy(col_max)
    temp_3 = np.copy(col_median)
    temp_4 = np.copy(col_positive)
    temp_1.sort()
    temp_2.sort()
    temp_3.sort()
    temp_4.sort()
    if shape[1] % 2 == 0:
        index = shape[1] // 2
        min_median = temp_1[index:index+2].mean()
        max_median = temp_2[index:index+2].mean()
        median_median = temp_3[index:index+2].mean()
        pos_median = temp_4[index:index+2].mean()
    else:
        index = shape[1] // 2 + 1
        min_median = temp_1[index]
        max_median = temp_2[index]
        median_median = temp_3[index]
        pos_median = temp_4[index]

    min_min = col_min.min()
    max_min = col_max.min()
    median_min = col_median.min()
    pos_min = col_positive.min()

    min_max = col_min.max()
    max_max = col_max.max()
    median_max = col_median.max()
    pos_max = col_positive.max()

    min_pos = (col_min>0).sum()
    max_pos = (col_max>0).sum()
    median_pos = (col_median>0).sum()
    pos_pos = (col_positive>0).sum()


    row_positive = np.array(range_num_row(data)).reshape(shape[0])
    row_max = data.max(axis=1).toarray().reshape(shape[0])
    row_median = []
    for i, m in enumerate(((data != 0).sum(1) > shape[1]//2).tolist(), 0):
        if m[0]:
            temp = data.getrow(i).toarray().reshape(data.shape[1],)
            row_median.append(np.median(temp))
        else:
            row_median.append(0)
    row_median = np.array(row_median)
    row_num_of_pos = np.array((data != 0).sum(1)).reshape(shape[0])

    row_pos_genes = []
    row_pos_genes.append(range_num(row_positive, 0))
    row_pos_genes.append(range_num(row_positive, 0, 1))
    index = 1
    while index<max(row_positive):
        row_pos_genes.append(range_num(row_positive, index, index*2))
        index *= 2

    col_pos_genes = []
    col_pos_genes.append(range_num(col_positive, 0))
    col_pos_genes.append(range_num(col_positive, 0, 1))
    index = 1
    while index<max(col_positive):
        col_pos_genes.append(range_num(col_positive, index, index*2))
        index *= 2

    with open(os.path.splitext(fn)[0] + '_statistic.csv', 'w') as w:
        w.write(',,min,median,max,num of pos,,num of barcodes,%d,,number of genes,%d\n'% (shape[1], shape[0]))
        w.write(',min,%d,%d,%d,%d\n' % (min_min,min_median,min_max,min_pos))
        w.write(',median,%d,%d,%d,%d\n' % (median_min,median_median,median_max,median_pos))
        w.write(',max,%d,%d,%d,%d\n' % (max_min,max_median,max_max,max_pos))
        w.write(',num of pos,%d,%d,%d,%d\n' % (pos_min,pos_median,pos_max,pos_pos))
        w.write('\nnum of col pos gene, num of cell,,\n')
        w.write('0,%d,%d\n' % (col_pos_genes[0], col_pos_genes[0]))
        temp = col_pos_genes[0]
        index = 1
        for i in col_pos_genes[1:]:
            temp+=i
            w.write('%d,%d,%d\n' % (index, i, temp))
            index *= 2


        w.write('\nnum of row pos gene, num of cell,,\n')
        w.write('0,%d,%d\n' % (row_pos_genes[0], row_pos_genes[0]))
        temp = row_pos_genes[0]
        index = 1
        for i in row_pos_genes[1:]:
            temp+=i
            w.write('%d,%d,%d\n' % (index, i, temp))
            index *= 2
            

if __name__ == '__main__':
        filename = util.get_file()
        print(filename)
        try:
            if os.path.splitext(filename)[1] == '.csv':
                print('Compressing...')
                data = compress.compress_file(filename, save=False)
                print('Statistic...')
                calculate(filename, data)
            elif os.path.splitext(filename)[1] == '.mtx':
                print('Statistic...')
                calculate(filename, scipy.io.mmread(filename))
            else:
                print('Statistic...')
                calculate(filename, sparse.load_npz(filename))
        except Exception as _:
            print('WARNING*******************************************\n', filename)
