def load_data(filename):
    with open(filename, 'r') as f:
        data = [int(i) for i in f.readline().strip().split(',')]
    return data

def simulate(input_list, days):
    occurances = [0] * 9
    for i in input_list:
        occurances[i] += 1

    for i in range(days):
        new = occurances[0]
        occurances[0:-1] = occurances[1:]
        occurances[-1] = new
        occurances[-3] += new

    return sum(occurances)

def pt_1(data):
    return simulate(data, 80)

def pt_2(data):
    return simulate(data, 256)

if __name__ == '__main__':
    data = load_data('input.txt')

    print(pt_1(data))
    print(pt_2(data))


