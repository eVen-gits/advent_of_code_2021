from enum import Enum

class Flag(Enum):
    A = 2 ** 6
    B = 2 ** 5
    C = 2 ** 4
    D = 2 ** 3
    E = 2 ** 2
    F = 2 ** 1
    G = 2 ** 0

class Digit:
    def __init__(self, value, nsegs, flags):
        self.value = value
        self.nsegs = nsegs
        self.flags = flags
        self.encoded = None

    def __repr__(self):
        return 'Digit {} - {:07b}={}'.format(self.value, self.flags, self.encoded)

DIGITS = {
    0: Digit(
        0, 6,
        Flag.A.value | Flag.B.value | Flag.C.value | Flag.E.value | Flag.F.value | Flag.G.value
    ),
    1: Digit(
        1, 2,
        Flag.C.value | Flag.F.value
    ),
    2: Digit(
        2, 5,
        Flag.A.value | Flag.C.value | Flag.D.value | Flag.E.value | Flag.G.value
    ),
    3: Digit(
        3, 5,
        Flag.A.value | Flag.C.value | Flag.D.value | Flag.F.value | Flag.G.value
    ),
    4: Digit(
        4, 4,
        Flag.B.value | Flag.C.value | Flag.D.value | Flag.F.value
    ),
    5: Digit(
        5, 5,
        Flag.A.value | Flag.B.value | Flag.D.value | Flag.F.value | Flag.G.value
    ),
    6: Digit(
        6, 6,
        Flag.A.value | Flag.B.value | Flag.D.value | Flag.E.value | Flag.F.value | Flag.G.value
    ),
    7: Digit(
        7, 3,
        Flag.A.value | Flag.C.value | Flag.F.value
    ),
    8: Digit(
        8, 7,
        Flag.A.value | Flag.B.value | Flag.C.value | Flag.D.value | Flag.E.value | Flag.F.value | Flag.G.value
    ),
    9: Digit(
        9, 6,
        Flag.A.value | Flag.B.value | Flag.C.value | Flag.D.value | Flag.F.value | Flag.G.value
    ),
}

class Decoder:
    DEFAULT_MAPPING = {
        Flag.A.value: None,
        Flag.B.value: None,
        Flag.C.value: None,
        Flag.D.value: None,
        Flag.E.value: None,
        Flag.F.value: None,
        Flag.G.value: None,
    }

    def __init__(self):
        self.mapping = None
        self.encoded = {}
        self.decoded = {}
        self.direct_len_mapping = {}
        self.reset()

    @property
    def sorted_encoded(self):
        return [v for _, v in sorted(self.encoded.items(), key=lambda x: x[0])]

    def reset(self):
        self.mapping = self.DEFAULT_MAPPING.copy()
        self.encoded = {
            0: None,
            1: Digit(1, 2, None),
            2: None,
            3: None,
            4: Digit(4, 4, None),
            5: None,
            6: None,
            7: Digit(7, 3, None),
            8: Digit(8, 7, None),
            9: None,
        }
        self.direct_len_mapping = {
            2: 1,
            4: 4,
            3: 7,
            7: 8,
        }
        self.decoded = {}

    def decode_line(self, line):
        self.reset()
        for i, encoded_digit in enumerate(line):
            #self.encoded[i] = digit
            self.direct_map(encoded_digit)
        print('\n'.join([str(x) for x in self.sorted_encoded if x]))
        for i, encoded_digit in enumerate(line):
            if encoded_digit in self.decoded.keys():
                continue
            else:
                self.smart_map(encoded_digit)
        return self.sorted_encoded

    def save_mapping(self, value, encoded):
        digit = self.encoded.get(value, Digit(value, len(encoded), None))
        if not digit.flags:
            digit.flags = 0
            for flag in encoded:
                digit.flags |= Flag[flag.upper()].value
            digit.encoded = encoded
            self.decoded[encoded] = digit

    def direct_map(self, encoded: str) -> bool:
        strlen = len(encoded)
        if len(encoded) in self.direct_len_mapping.keys():
            self.save_mapping(self.direct_len_mapping[strlen], encoded)
            return True
        return False

    def smart_map(self, encoded: str) -> bool:
        strlen = len(encoded)
        # find digits that have same length
        candidates = [digit for digit in DIGITS.values() if digit.nsegs == strlen]
        if len(candidates) == 1:
            self.save_mapping(candidates[0].value, encoded)
        else:
            # calculate flags from encoded string
            flags = 0
            for flag in encoded:
                flags |= Flag[flag.upper()].value
            print(self.sorted_encoded)


def pt_1(data):
    count = 0
    valid_nsegs = [d.nsegs for d in DIGITS.values() if d.value in [1, 4, 7, 8]]
    for din, dout in data:
        for i_out in dout:
            if len(i_out) in valid_nsegs:
                count +=1
    return count

def pt_2(data):
    decoder = Decoder()
    for d in data:
        decoder.decode_line(d)

if __name__ == '__main__':
    with open('demo.txt', 'r') as f:
        data = [i.strip() for i in f.readlines()]
        data_in = []
        data_out = []
        for line in data:
            line_in, line_out = line.split(' | ')
            data_in.append(line_in.split(' '))
            data_out.append(line_out.split(' '))
        data = [data_in + data_out for data_in, data_out in zip(data_in, data_out)]
    pt_2(data)

    #print(pt_1(data))