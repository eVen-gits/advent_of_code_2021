from enum import Enum

def bin2str(num: int) -> str:
    return '{:07b}'.format(num)[::-1]

def sum_bits(num: int) -> int:
    # sum set bits of num in binary format
    return sum([1 for x in bin2str(num) if x == '1'])

class Flag(Enum):
    A = 2 ** 0
    B = 2 ** 1
    C = 2 ** 2
    D = 2 ** 3
    E = 2 ** 4
    F = 2 ** 5
    G = 2 ** 6

class Digit:
    def __init__(self, value, nsegs, flags):
        self.value = value
        self.nsegs = nsegs
        self.flags = flags

    def __repr__(self):
        return 'Digit {} - {}={}'.format(self.value, bin2str(self.flags) if self.flags else '')

class Decoder:
    DIRECT_LEN_MAPPING = {
        2: 1,
        4: 4,
        3: 7,
        7: 8,
    }

    # first key is length of the encoded string
    # second key is the sum of the set bits in flags
    # value is the digit value
    IMPLICIT_MAPPING = {
        5: {
            14: 2,
            8:  3,
            12: 5,
        },
        6: {
            11:0,
            15:6,
            9: 9,
        },
    }

    def __init__(self):
        self.mapping = None
        self.encoded = {}
        self.decoded = {}

        self.reset()

    @property
    def sorted_encoded(self):
        return [v for _, v in sorted(self.encoded.items(), key=lambda x: x[0])]

    def reset(self):
        self.encoded = {}
        for key, val in DIGITS.items():
            self.encoded[key] = Digit(val.value, val.nsegs, None)
        self.decoded = {}

    def decode(self, encoded: str) -> str:
        flags = self.calculate_flags(encoded)
        if flags in self.decoded.keys():
            return self.decoded[flags].value
        else:
            return '?'

    def decode_line(self, line):
        self.reset()
        for i, encoded_digit in enumerate(line):
            self.direct_map(encoded_digit)

        for i, encoded_digit in enumerate(line):
            flags = self.calculate_flags(encoded_digit)
            if flags not in self.decoded.keys():
                if not self.smart_map(encoded_digit):
                    print('Could not decode {}'.format(encoded_digit))

        return int(''.join(map(str, [self.decode(enc) for enc in line[-4:]])))

    def calculate_flags(self, value: str) -> int:
        flags = 0
        for flag in value:
            flags |= Flag[flag.upper()].value
        return flags

    def save_mapping(self, value, encoded):
        digit = self.encoded.get(value, Digit(value, len(encoded), None))
        if not digit.flags:
            digit.flags = self.calculate_flags(encoded)
            self.decoded[digit.flags] = digit

    def direct_map(self, encoded: str) -> bool:
        strlen = len(encoded)
        if len(encoded) in self.DIRECT_LEN_MAPPING.keys():
            self.save_mapping(self.DIRECT_LEN_MAPPING[strlen], encoded)
            return True
        return False

    def smart_map(self, encoded: str) -> bool:
        strlen = len(encoded)

        # calculate flags from encoded string
        flags = self.calculate_flags(encoded)
        xor_sum = sum([sum_bits(self.encoded[x].flags ^ flags) for x in [1, 4, 7]])

        try:
            value = self.IMPLICIT_MAPPING[strlen][xor_sum]
        except KeyError:
            return False
        self.save_mapping(value, encoded)
        return True

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

# Check for unique mappings
# This could be done automatically to derrive general solution
'''for a in [2, 3, 5, 0, 6, 9]:
    print(a)
    for b in [1, 4, 7]:
        xor = DIGITS[a].flags ^ DIGITS[b].flags
        print('  {} = {} -> {}'.format(b, bin2str(xor), sum_bits(xor)))
'''


def pt_1(data):
    count = 0
    valid_nsegs = [d.nsegs for d in DIGITS.values() if d.value in [1, 4, 7, 8]]
    for line in data:
        for i_out in line[-4:]:
            if len(i_out) in valid_nsegs:
                count +=1
    return count

def pt_2(data):
    decoder = Decoder()
    return sum([decoder.decode_line(d) for d in data])


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        data = [i.strip() for i in f.readlines()]
        data_in = []
        data_out = []
        for line in data:
            line_in, line_out = line.split(' | ')
            data_in.append(line_in.split(' '))
            data_out.append(line_out.split(' '))
        data = [data_in + data_out for data_in, data_out in zip(data_in, data_out)]

    print(pt_1(data))
    print(pt_2(data))