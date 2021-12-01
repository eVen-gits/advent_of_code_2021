
def pt_0(data):
    descends = sum([
        1 for
        i in range(1, len(data))
        if data[i] > data[i-1]
    ])
    return descends

def pt_1(data):
    return sum([
        1 if sum(data[i:i+3]) < sum(data[i+1:i+4]) else 0
        for i in range(0, len(data)-3)
    ])

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
            data = [int(i) for i in f.readlines()]
    print(pt_0(data))
    print(pt_1(data))