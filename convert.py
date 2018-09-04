import numpy as np
from scipy import sparse as sp


def standardize(genes, data, mappings):
    ensg_genename = {}
    genename_index = {}
    for i in mappings:
        line = i.replace('\n', '').split(',')
        ensg_genename[line[0]] = 'hg38_' + line[1][1:]
        genename_index['hg38_' + line[1][1:]] = []
        
    for i in range(len(genes)):
        temp = genes[i]
        if temp in ensg_genename:
            genename_index[ensg_genename[temp]].append(i)

    print('Building sparse matrix...')
    rows = []
    count = 0
    for i in genename_index.keys():
        if len(genename_index[i])==0:
            count+=1
            temp = np.zeros(data.shape[1])
            temp = sp.csr_matrix(temp, dtype=np.int32)
            temp.eliminate_zeros()
        elif len(genename_index[i])==1:
            temp = data.getrow(genename_index[i][0])
        else:
            temp = data.getrow(genename_index[i][0]).toarray()
            for x in genename_index[i][1:]:
                temp += data.getrow(x).toarray()
            temp = sp.csr_matrix(temp, dtype=np.int32)
            temp.eliminate_zeros()
        rows.append(temp)

    new_data  = sp.vstack(rows)
    new_data = sp.csc_matrix(new_data, dtype=np.int32)
    genes = list(genename_index.keys())

    print(count)

    return new_data, genes