import time
from scipy import sparse
import multiprocessing
from multiprocessing import Pool
import os
import tkinter.filedialog
from tkinter import *


def get_data2(content):
    indptr = [0]
    indices = []
    data = []
    for line in content:
        line = line.replace('\n', '').split(',')
        temp = ([float(i) for i in line[1:]])
        count = 0
        for i in range(len(temp)):   
            if temp[i] != 0:
                count += 1
                indices.append(i)
                data.append(temp[i])
        indptr.append(indptr[-1] + count)
    return indptr, indices, data


def demo(fn):
    data_set = []
    f = open(fn, encoding='UTF-8')

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

    sparse.save_npz('csc_sparse.npz', c)


def get_file():
    root = Tk()
    default_dir = r"C:\Users\Minjie LYU\Desktop\benchmark"  # default dir
    fname = tkinter.filedialog.askopenfilename(title=u"Chose a File",
                                     initialdir=(os.path.expanduser(default_dir)))
    root.destroy()
    return fname


def main():
    fn = get_file()
    num = 3
    print('num', num)
    s = time.time()
    l = time.time()
    for _ in range(num):
        demo(fn)
        print(time.time() - l)
        l = time.time()
    e = time.time()

    print('average time', (e-s)/num)
    print('total time', e-s)


if __name__ == '__main__':
    main()
