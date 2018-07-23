import scipy.sparse as sp
import util
import time

def npz_to_csv(file_name, file_row_head='genes.txt'):
    output_file = file_name.split('.')[0]+'.csv'
    spr = sp.csr_matrix(sp.load_npz(file_name), dtype=int)
    with open(file_row_head) as rh:
        row_heads = list(map(lambda x: x.replace('\n', ''), rh.readlines()))

    with open(output_file, 'w') as f:
        s = time.time()
        f.write(str(list(range(spr.shape[1]+1)))[1:-1].replace(' ','') + '\n')
        for i in range(spr.shape[0]):
            f.write(row_heads[i] + ',' + str(spr.getrow(i).toarray()[0].tolist())[1:-1].replace(' ', ''))
            f.write('\n')
        print(time.time() - s)

def main():
    file_name = util.get_file()
    npz_to_csv(file_name)

if __name__ == '__main__':
    main()