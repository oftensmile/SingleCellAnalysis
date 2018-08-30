import numpy as np
from scipy import sparse as sp
import os

def calculate(fn):
    spr = sp.load_npz(fn)
    number_of_cells = spr.shape[1]
    sum_of_cols = np.squeeze(np.array(spr.sum(axis=0)))
    no_of_pos = np.squeeze(np.array((spr != 0).sum(0)))
    p_minimum = min(no_of_pos)
    p_maximum = max(no_of_pos)
    p_median = np.median(no_of_pos)
    t_minimum = min(sum_of_cols)
    t_maximum = max(sum_of_cols)
    t_median = np.median(sum_of_cols)
    transcripts_sum = spr.sum()
    transcripts_sum_per_cell = int(transcripts_sum / number_of_cells)
    density = len(spr.data) / (spr.shape[0] * spr.shape[1])
    sparsity = 1-density

    return number_of_cells, p_minimum, p_maximum, p_median, t_minimum, t_maximum, t_median, transcripts_sum, transcripts_sum_per_cell, density, sparsity


def main():
    files = os.listdir()
    with open('results.csv', 'w') as res:
        res.write(",,,POSITIVES,,,TRANSCRIPTS\n")
        res.write("File name, Number of cells, Minimum, Maximum, Median, Minimum, Maximum, Median, Sum of Transcripts, Sum of Transcripts per cell, Density, Sparsity\n")
        for file in files:
            print(file)
            if 'npz' in file:
                number_of_cells, p_minimum, p_maximum, p_median, t_minimum, t_maximum, t_median, transcripts_sum, transcripts_sum_per_cell, density, sparsity = calculate(file)
                res.write(file + ',' + str(number_of_cells) + ',' + str(p_minimum) + ',' + str(p_maximum) + ',' + str(p_median) + ',' + str(t_minimum) + ',' + str(t_maximum) + ',' + str(t_median) + ',' + str(transcripts_sum) + ',' + str(transcripts_sum_per_cell) + ',' + str(density) + ',' + str(sparsity) +'\n')


if __name__ == '__main__':
    main()