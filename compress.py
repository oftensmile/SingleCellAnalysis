import csv
import numpy as np
import time
from scipy import sparse
from multiprocessing import Pool


def func(filename, start_index, end_index):
    test = []
    with open(filename) as content:
        for i, line in enumerate(content):
            if(i >= start_index and i < end_index):
                line = line.replace('\n', '').split(',')
                temp = sparse.csr_matrix(line[1:], dtype=float)
                temp.eliminate_zeros()
                test.append(temp)
            elif(i == end_index):
                break
    x = sparse.vstack(test)
    return x


def demo(fn):
    filename = fn
    num_lines = sum(1 for line in open(filename))

    length = num_lines // 4
    index = []
    for i in range(4):
        index.append(length * i)
    index.append(num_lines)
    index[0]=1

    p = Pool(4)
    res_l =[]
    for i in range(4):
        res = p.apply_async(func, args=('original.csv', index[i], index[i+1]))
        res_l.append(res)
    p.close()
    p.join()

    x = []
    for i in range(4):
        tmp = res_l[i].get()
        x.append(tmp)
    
    data = sparse.vstack(x)
    sparse.save_npz(filename.split('.')[0] + '.npz',  data.tocsc())


def main():
    num = 3
    print('num', num)
    s = time.time()
    l = time.time()
    for _ in range(num):
        demo('original.csv')
        print(time.time() - l)
        l = time.time()
    e = time.time()

    print('average time', (e-s)/num)
    print('total time', e-s)

if __name__ == '__main__':
    main()

