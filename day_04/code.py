from copy import deepcopy

def load_data(filename):
    with open(filename, 'r') as f:
        data = [i for i in f.readlines()]
    rng = [int(i) for i in data[0].split(',')]
    del data[0:2]

    return data, rng

class Game:
    def __init__(self, rng):
        self.boards = []
        self.rng = rng

    def done(self):
        return all([board.done for board in self.boards])

    def play_pt1(self):
        for num in self.rng:
            for board in self.boards:
                board.cross(num)
                if board.check_win():
                    return num * board.sum_remaining()

    def play_pt2(self):
        for num in self.rng:
            for board in self.boards:
                if not board.done:
                    board.cross(num)
                    if board.check_win():
                        if self.done():
                            return num * board.sum_remaining()
        return None

class Board:
    def __init__(self, data,):
        self.done = False
        self.unmarked = []
        self.parse(data)
        self.marked = []

    def parse(self, data):
        for line in data:
            if len(line.strip()) == 0:
                continue
            row = [int(val) for val in line.strip().split()]
            self.unmarked.append(row)

    def cross(self, num):
        for row in self.unmarked:
            for i, val in enumerate(row):
                if val == num:
                    row[i] = None
                    self.marked.append(num)
                    return

    def check_win(self):
        if len(self.marked) < 5:
            return False
        for row in self.unmarked:
            for i in range(5):
                if row[i] is not None:
                    break
            else:
                self.done = True
                return True

        for i in range(5):
            for row in self.unmarked:
                if row[i] is not None:
                    break
            else:
                self.done = True
                return True

        return False

    def sum_remaining(self):
        sum_numbers = 0
        for row in self.unmarked:
            sum_numbers += sum([col for col in row if col is not None])
        return sum_numbers

    def __repr__(self):
        out_str = ''
        for i in range(5):
            for j in range(5):
                if self.unmarked[i][j] is None:
                    out_str += '.'.ljust(3)
                else:
                    out_str += str(self.unmarked[i][j]).ljust(3)
            out_str += '\n'
        return out_str

def pt_1(data, rng):
    game = Game(rng)
    for _ in range((len(data)+1) // 6):
        game.boards.append(Board(data[:6]))
        del data[:6]

    winner = game.play_pt1()
    return winner


def pt_2(data, rng):
    game = Game(rng)
    for _ in range((len(data)+1) // 6):
        game.boards.append(Board(data[:6]))
        del data[:6]

    loser = game.play_pt2()
    return loser

if __name__ == '__main__':
    data, rng = load_data('input.txt')

    print(pt_1(deepcopy(data), deepcopy(rng)))
    print(pt_2(deepcopy(data), deepcopy(rng)))