filenames = ['001_10k.csv','002_10k.csv','003_10k.csv','004_10k.csv','005_10k.csv','006_10k.csv',
             '007_10k.csv','008_10k.csv','009_10k.csv','010_10k.csv','011_10k.csv','012_10k.csv',
             '013_10k.csv','014_10k.csv','015_10k.csv','016_10k.csv','017_10k.csv','018_10k.csv',
             '019_10k.csv','020_10k.csv','021_10k.csv','022_10k.csv','023_10k.csv','024_10k.csv',
             '025_10k.csv','026_10k.csv','027_10k.csv','031_10k.csv','032_10k.csv','033_10k.csv',
             '034_10k.csv','S1_10k.csv','S2_10k.csv','S7_10k.csv','S8_10k.csv',]
for filename in filenames:
    print(filename)
    fn = open(filename, encoding='utf-8')
    data = fn.readlines()
    columns = 20000
    col = len(data[0].replace('\n', '').split(',')) - 1
    if col <= columns:
        with open(filename[:3]+'_20k.csv', 'w', encoding='utf-8') as f:
            times = columns // col
            mods = columns % col
            f.write(data[0])
            for i in range(1, len(data)):
                data[i] = data[i].replace('\n', '').split(',')
                temp = data[i][1:]
                for time in range(times-1):
                    data[i].extend(temp)
                data[i].extend(temp[:mods])
                data[i].append('\n')
                line = ','.join(str(x) for x in data[i])
                f.write(line[:-2]+'\n')
    else:
        with open(filename[:3]+'_20k.csv', 'w', encoding='utf-8') as f:
            f.write(data[0])
            for i in range(1, len(data)):
                data[i] = data[i].replace('\n', '').split(',')
                data[i] = data[i][:10001]
                data[i].append('\n')
                line = ','.join(str(x) for x in data[i])
                f.write(line[:-2]+'\n')