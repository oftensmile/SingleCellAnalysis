def save_row_head(file):
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
    with open(file) as f:
        data = f.readlines()
        data = data[1:]
        row_head = []
        for line in data:
            row_head.append(line[:line.index(',')])
    
    return row_head