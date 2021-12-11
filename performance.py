import os
from time import time
from tqdm import tqdm
from copy import deepcopy

SAMPLE_RUNS = 100

if __name__ == '__main__':
    avg_times = []
    for day in range(1, 32):
        folder = 'day_{:02d}'.format(day)
        if not os.path.exists(folder):
            break

        import_str = '.'.join([
            folder,
            'code'
        ])
        relative_import = __import__(import_str, fromlist=[''])
        pt_1 = 0
        data = relative_import.load_data(os.path.join(folder, 'input.txt'))
        for i in tqdm(range(SAMPLE_RUNS), desc='Day {} part 1'.format(day)):
            try:
                start = time()
                relative_import.pt_1(deepcopy(data))
                end = time()
            except TypeError:
                start = time()
                relative_import.pt_1(*deepcopy(data))
                end = time()
            pt_1  += end - start
        pt_1 /= SAMPLE_RUNS

        pt_2 = 0
        for i in tqdm(range(SAMPLE_RUNS), desc='Day {} part 2'.format(day)):
            try:
                start = time()
                relative_import.pt_2(deepcopy(data))
                end = time()
            except TypeError:
                start = time()
                relative_import.pt_2(*deepcopy(data))
                end = time()
            pt_2  += end - start
        pt_2 /= SAMPLE_RUNS
        avg_times.append((pt_1, pt_2))
    for day, times in enumerate(avg_times):
        print('Day {} average times:\tpt_1 = {:0.03f}s\tpt_2 = {:0.03f}s'.format(str(day).ljust(2), times[0], times[1]))
