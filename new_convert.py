import numpy as np
import h5py
from scipy import sparse
import scipy.io
import compress
import save_row_head
import time
import os
import sys


def get_genes_and_data(filename):
    genes = save_row_head.return_row_head(filename)
    data = compress.compress_file(filename, save=False)
    new_genes, new_data = standardize(genes, data)
    return new_genes, new_data


def standardize(genes, data):
    f = open('convert_mapping.csv')
    temp = f.readlines()
    ensg_genename = {}
    genename_index = {}
    for i in temp:
        line = i.replace('\n', '').split(',')
        ensg_genename[line[0]] = 'hg38_' + line[1][1:]
        genename_index['hg38_' + line[1][1:]] = []
        
    rest = {}
    for i in range(len(genes)):
        temp = genes[i]
        if temp in ensg_genename:
            genename_index[ensg_genename[temp]].append(i)
        else:
            rest[temp] = i

    print('Duplicating...')
    long = data.shape[1]
    test = []
    count = 0
    for i in genename_index.keys():
        if len(genename_index[i])==0:
            count+=1
            temp = np.zeros(long)
            temp = sparse.csr_matrix(temp, dtype=int)
            temp.eliminate_zeros()
        elif len(genename_index[i])==1:
            temp = data.getrow(genename_index[i][0])
        else:
            temp = data.getrow(genename_index[i][0]).toarray()
            for x in genename_index[i][1:]:
                temp += data.getrow(x).toarray()
            temp = sparse.csr_matrix(temp, dtype=int)
            temp.eliminate_zeros()
        test.append(temp)

    new_data  = sparse.vstack(test)
    new_data = sparse.csc_matrix(new_data, dtype=int)
    genes = list(genename_index.keys())

    print(count)

    return genes, new_data


def save_csv(save_path, data, genes):
    data = data.tocsr()
    with open(save_path + 'csv.csv', 'w') as f:
        for i in range(1, data.shape[1]+1):
            f.write(',%d' % i)
        f.write('\n')
        for i in range(data.shape[0]):
            f.write(genes[i] + ',' + str(data.getrow(i).toarray()[0].tolist())[1:-1].replace(' ', '') + '\n')


def save_mtx(save_path, data, genes, barcodes=None):
    #save mtx
    scipy.io.mmwrite(save_path + 'mtx.mtx', data)

    #save genes
    with open(save_path + 'genes.tsv', 'w') as f:
        for i in genes:
            f.write(i + '\n')

    #save barcodes
    with open(save_path+'barcodes.tsv', 'w') as f:
        if barcodes:
            for i in barcodes:
                f.write(i + '\n')
        else:
            for i in range(1, data.shape[1]+1):
                f.write(str(i) + '\n')


def save_h5(save_path, data, genes, barcodes=None):
    if not barcodes:
        barcodes = np.array(range(1, data.shape[1]+1), dtype='S')

    with h5py.File(save_path + 'h5.h5', 'w') as hf:
        group = hf.create_group('sct')
        group.create_dataset('barcodes', data=barcodes)
        group.create_dataset('gene_names', data=np.array(genes, dtype='S'))
        group.create_dataset('data', data=data.data)
        group.create_dataset('indices', data=data.indices)
        group.create_dataset('indptr', data=data.indptr)
        group.create_dataset('shape', data=data.shape)


def save_all(save_path, data, genes):
    s = time.time()
    sparse.save_npz(save_path + 'npz.npz',  data)
    print(time.time() - s)

    s = time.time()
    save_csv(save_path, data, genes)
    print(time.time() - s)

    s = time.time()
    save_mtx(save_path, data, genes)
    print(time.time() - s)

    s = time.time()
    save_h5(save_path, data, genes)
    print(time.time() - s)

def main(filename):
    save_path = os.path.join(os.path.dirname(os.path.abspath(filename)), 'convert', os.path.splitext(os.path.split(filename)[1])[0][:-3])
    
    s = time.time()
    genes, data = get_genes_and_data(filename)
    print(time.time() - s)
    
    save_all(save_path, data, genes)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: " + sys.argv[0] + " FILENAME")
        sys.exit(1)
    main(sys.argv[1])
