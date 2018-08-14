import scipy.sparse as sp
import scipy.io
import util
import time

def sparse_to_csv(spr, row_heads, output_file):
    spr = spr.tocsr()
    with open(output_file, 'w') as f:
        f.write('Index,' + str(list(range(1, spr.shape[1])))[1:-1].replace(' ', '') + '\n')

        for i in range(spr.shape[0]):
            f.write(row_heads[i] + ',' + str(spr.getrow(i).toarray()[0].tolist())[1:-1].replace(' ', '') + '\n')


def get_data_from_files(file_name, file_row_head='genes.tsv', file_barcodes=None, isMtx=True):
    if isMtx:
        output_file = str(file_name.split('.')[:-1])[2:-2]
    else:
        output_file = str(file_name.split('.')[:-1])[2:-2] + '.csv'

    if isMtx:
        spr = sp.csr_matrix(scipy.io.mmread(file_name), dtype=int)
    else:
        spr = sp.csr_matrix(sp.load_npz(file_name), dtype=int)

    if file_barcodes:
        with open(file_barcodes) as bar:
            barcodes = list(map(lambda x: x.replace('\n', ''), bar.readlines()))
    else:
        barcodes = None

    with open(file_row_head) as rh:
        if isMtx:
            row_heads = list(map(lambda x: x.replace('\n', '').split('\t')[1], rh.readlines()))
        else:
            row_heads = list(map(lambda x: x.replace('\n', ''), rh.readlines()))

    return spr, row_heads, barcodes, output_file


def find_splits(barcodes):
    splits = []
    i = 0
    for num, b in enumerate(barcodes):
        if b.split('-')[1] != str(i):
            i+=1
            splits.append(num)
    return splits


def split_and_convert(spr, row_heads, barcodes, output_file='output'):
    splits = find_splits(barcodes)
    length = len(splits)
    for s in range(length):
        if s+1 < length:
            sparse_mat = spr.tocsc()[:, splits[s]:splits[s+1]]
        else:
            sparse_mat = spr.tocsc()[:, splits[s]:]
        out = output_file + '_' + str(s+1) + '.csv'
        sparse_to_csv(sparse_mat, row_heads, out)
    

def main():
    file_name = util.get_file("Select mtx or npz file")
    if file_name.split('.')[-1] == 'mtx':
        isMtx = True
    else:
        isMtx = False

    file_row_head = util.get_file("Select gene names")
    file_barcodes = util.get_file("Select barcodes file")

    spr, row_heads, barcodes, output_file = get_data_from_files(file_name, file_row_head, file_barcodes, isMtx)

    split_and_convert(spr, row_heads, barcodes, output_file)

if __name__ == '__main__':
    main()