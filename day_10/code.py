CLOSING = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

ERROR_SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

FIX_SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

OPENING = [
    '(',
    '[',
    '{',
    '<',
]

DEBUG = False

def load_data(filename):
    with open(filename, 'r') as f:
        data = [i.strip() for i in f.readlines()]
    return data

class IncompleteLineException(Exception):
    pass

def print_marker(line, i, j, marker='|'):
    print('{}\n{}{}'.format(line, marker.rjust(i+1), marker.rjust(j-i)))


def parse(line, start, stop, throw_exception=False):
    errors = []
    i = start+1
    if start == stop:
        return start, errors
    while i < stop:
        if DEBUG: print_marker(line, start, i)
        if line[i] in OPENING:
            j, ret_errors = parse(line, i, stop, throw_exception=throw_exception)
            if DEBUG: print_marker(line, i, j, marker='*')
            i = j + 1
            for e in ret_errors:
                errors.append(e)

        elif line[i] == CLOSING[line[start]]:
            if start > 0:
                return i, errors # no error
            else:
                return parse(line, i+1, stop, throw_exception=throw_exception)
        elif line[i] in CLOSING.values():
            if DEBUG: print_marker(line, start, i, marker='!')
            errors.append((CLOSING[line[start]], line[i]))
            return i, errors
    if throw_exception:
        if DEBUG: print_marker(line, start, i, marker='?')
        raise IncompleteLineException(line[start])
    else:
        return i, errors


def pt_1(data):
    score = 0
    for line in data:
        try:
            _, errors = parse(line, 0, len(line))
            if errors:
                score += sum(ERROR_SCORES[f] for e, f in errors)
                e, f = errors[0]
                if DEBUG: print('{} - Expected {}, but found {} instead.'.format(line, e, f))
        except IncompleteLineException as e:
            if DEBUG: print(e)
    return score

def pt_2(data):
    scores = []
    for line in data:
        _, errors = parse(line, 0, len(line))
        if not errors:
            score = 0
            fix = ''
            while True:
                try:
                    if DEBUG: print(line+fix)
                    parse(line+fix, 0, len(line+fix), throw_exception=True)
                    break
                except IncompleteLineException as e:
                    if DEBUG: print('Adding', CLOSING[e.args[0]])
                    fix += CLOSING[e.args[0]]

            if DEBUG: print('{} - Complete by adding {}'.format(line, fix), end='')
            for correciton in fix:
                score = score * 5 + FIX_SCORES[correciton]
            scores.append(score)
            if DEBUG: print(' - {} total points.'.format(score))

    return sorted(scores)[len(scores)//2]

if __name__ == '__main__':
    data = load_data('input.txt')
    print(pt_1(data))
    print(pt_2(data))