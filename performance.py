import os
from time import time

SAMPLE_RUNS = 100

if __name__ == '__main__':
    for day in range(1, 31):
        folder = 'day_{:02d}'.format(day)
        if not os.path.exists(folder):
            break

        import_str = '.'.join([
            folder,
            'code'
        ])
        relative_import = __import__(import_str, fromlist=[''])
        pt_1 = 0
        for i in range(SAMPLE_RUNS):
            data = relative_import.load_data(os.path.join(folder, 'input.txt'))
            try:
                start = time()
                relative_import.pt_1(data)
                end = time()
            except TypeError:
                start = time()
                relative_import.pt_1(*data)
                end = time()
            pt_1  += end - start
        pt_1 /= SAMPLE_RUNS

        pt_2 = 0
        for i in range(SAMPLE_RUNS):
            data = relative_import.load_data(os.path.join(folder, 'input.txt'))
            try:
                start = time()
                relative_import.pt_2(data)
                end = time()
            except TypeError:
                start = time()
                relative_import.pt_2(*data)
                end = time()
            pt_2  += end - start
        pt_2 /= SAMPLE_RUNS

        print('Avreage time: {:0.03f}\t{:0.03f}'.format(pt_1, pt_2))
