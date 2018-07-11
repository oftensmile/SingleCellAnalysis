import scipy.sparse as sp
import util
import time

file_name = util.get_file()
output_file = file_name.split('.')[0]+'.csv'
spr = sp.csr_matrix(sp.load_npz(file_name), dtype=int)

with open(output_file, 'w') as f:
    s = time.time()
    for i in range(spr.shape[0]):
        f.write(str(spr.getrow(i).toarray()[0].tolist())[1:-1].replace(' ', ''))
        f.write('\n')
    print(time.time() - s)
