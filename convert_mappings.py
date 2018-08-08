import time
import util

def convert_mappings(input_file, mappings_file, from_map_id=0, to_map_id=1):
    output_file = ''.join(input_file.split('.')[:-1]) + '_converted.' + input_file.split('.')[-1]

    if input_file.split('.')[-1] == 'csv':
        delimeter = ','
    else:
        delimeter = '\t'

    with open(mappings_file) as mappings:
        m = list(map(lambda x : x.replace('\n', '').split(delimeter), mappings.readlines()))

    from_map = [line[from_map_id] for line in m]
    to_map = [line[to_map_id] for line in m]

    with open(output_file, 'w') as output:
        with open(input_file) as data:
            output.write('Index,' + str(list(range(1, len(data.readline().split(',')))))[1:-1].replace(' ', '') + '\n')
        with open(input_file) as data:
            err = 0
            for row in data:
                x = row.replace('\n', '').split(delimeter)
                try:
                    x[0] = to_map[from_map.index(x[0])]
                    output.write(str(x).replace('\'', '').replace(' ', '')[1:-1] + '\n')
                except ValueError:
                    # output.write(row)
                    err += 1
                    print(x[0])
                    continue
    
    print(err)

def main():
    input_file = util.get_file()
    mappings_file = util.get_file()
    num = 1
    print('num', num)
    s = time.time()
    l = time.time()
    for _ in range(num):
        convert_mappings(input_file, mappings_file, 0, 1)
        print(time.time() - l)
        l = time.time()
    e = time.time()

    print('average time', (e-s)/num)
    print('total time', e-s)

if __name__ == '__main__':
    main()