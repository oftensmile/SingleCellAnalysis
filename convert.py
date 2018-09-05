import numpy as np
from scipy import sparse as sp
import util

GENE_TO_ENSG = 'hg19_hg38.csv'


def standardize(genes, data, mappings):
    '''
       1. Select genes in the standard list 
       2. Sum and remove the duplicate genes
       3. Reorder the genes (same as mapping file)   
    Arguments:
        genes {list} -- the list of ENSG (not standardized)
        data {scipy.sprase} -- the compressed sprarse matrix
        mappings {list} -- contain in the mapping file
    
    Returns:
        scipy.sparse.csc_matrix -- standardized data
        list -- standardized gene list (starts with hg38_) 
    '''

    genes = standardize_genes(genes)

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


def standardize_genes(genes):
    '''Convert the genes from various formats to ENSG
    
    Arguments:
        genes {list} -- list of genes read from input file
    
    Returns:
        list -- list of ENSG genes
    '''

    new_genes = []

    if "ENSG" in genes[0]:
        if len(genes[0]) != 15:
            if genes[0].index("ENSG") == 0:
                new_genes = list(map(lambda x: x[:15], genes))
            else:
                new_genes = list(map(lambda x: x[-15:], genes))
        else:
            new_genes = genes
    else:
        new_genes = genes_to_ensg(genes)
    return new_genes


def genes_to_ensg(genes):
    '''Convert the list of genes names to list of ENSG.
    
    Arguments:
        genes {list} -- list of genes to be converted to ENSG
    
    Returns:
        list -- list of ENSG values converted from genes
    '''

    try:
        f = open(GENE_TO_ENSG)
    except FileNotFoundError as _:
        f = util.get_file("Select mappings file")
    
    m = list(map(lambda x : x.replace('\n', '').split(','), f.readlines()))

    from_map = [line[1] for line in m]
    to_map = [line[0] for line in m]

    ensg = []

    for gene in genes:
        try:
            ensg.append(to_map[from_map.index(gene)])
        except ValueError as _:
            ensg.append(gene)

    f.close()

    return ensg
