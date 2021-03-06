#!/usr/bin/env python

__author__ = "Razin Shaikh and Minjie Lyu"
__credits__ = ["Razin Shaikh", "Minjie Lyu", "Vladimir Brusic"]
__version__ = "1.0"
__status__ = "Prototype"

def save_row_head(file):
    '''Saves the row head(gene names / ENSG) from CSV file'''
    with open(file) as f:
        data = f.readlines()
        data = data[1:]
        row_head = []
        for line in data:
            row_head.append(line[:line.index(',')])
        with open(file.split('.')[0] + '_row.txt', 'w') as f:
            for i in row_head:
                f.write(i + '\n')
    
    return file.split('.')[0] + '_row.txt'

def return_row_head(file):
    '''Returns the row head(gene names / ENSG) from CSV file'''
    with open(file) as f:
        data = f.readlines()
        data = data[1:]
        row_head = []
        for line in data:
            row_head.append(line[:line.index(',')])
    
    return row_head