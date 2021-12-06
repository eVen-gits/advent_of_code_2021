
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

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        data = [int(i) for i in f.readline().strip().split(',')]

    population = simulate(data, 80)
    print(population)
    population = simulate(data, 256)
    print(population)


