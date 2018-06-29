import psutil
import os
import compress
import compress_V1
import util


if __name__ == '__main__':
    fn = util.get_file()
    size = os.path.getsize(fn)
    available = psutil.virtual_memory()[1] / 2
    if size * 2 >= available:
        print('Compress 2 starting')
        compress.compress_file(fn)
    else:
        print('Compress 1 starting')
        compress_V1.compress_file(fn)


