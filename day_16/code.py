import sys
from enum import Enum

class MessageType(Enum):
    OPERATOR = 0
    LITERAL = 4

DEBUG = False
DEPTH = 0


def hex2bin(hex_str: str) -> str:
    return bin(int(hex_str, 16))[2:]

def bin2hex(bin_str: str) -> str:
    return hex(int(bin_str, 2))[2:]

def load_data(filename):
    with open(filename, 'r') as f:
        data = [
            ''.join([
                hex2bin(bit4).zfill(4)
                for bit4
                in line.strip()
            ])
            for line in f.readlines()
        ]
    return data

def parse_literal(data: list) -> (int, int):
    idx = 0
    field = data[idx:idx+5]
    number = ''
    while True:
        number += field[1::]
        if field[0] == '0':
            break
        idx += 5
        field = data[idx:idx+5]

    return int(number, 2), idx+5

def parse_operator(data: list):
    global DEPTH
    length_type_id = data[0] == '1'
    idx = 1
    messages = []
    if not length_type_id:
        end_idx = 16 + int(data[idx:idx+14], 2)
        print('{}<immediate len={}>\n{}{} {} {}'.format(
            '\t'*DEPTH,
            end_idx-16,
            '\t'*DEPTH,
            data[0],
            data[idx:idx+15],
            data[idx+15:end_idx]
        ))
        idx += 15
        DEPTH += 1
        print('{}immediate values='.format('\t'*DEPTH), end='')
        while idx < end_idx:
            val, msg_len = parse_literal(data[idx:end_idx])
            print(' {}'.format(val), end=' ')
            idx += msg_len + 1
        print()
        DEPTH -= 1
    else:
        number_of_subpackets_immediately_contained = int(data[idx:idx+11], 2)
        print('{}<nested={}>\n{}{} {} {}'.format(
            '\t'*DEPTH,
            number_of_subpackets_immediately_contained,
            '\t'*DEPTH,
            data[0],
            data[idx:idx+11],
            data[idx+11:]
        ))
        idx += 11
        DEPTH += 1
        for i in range(number_of_subpackets_immediately_contained):
            messages += parse(data[idx:])
            idx += messages[-1][-1] + 1
        DEPTH -= 1
    return messages


def parse(data: list):
    global DEPTH
    version = int(data[0:3], 2)
    msg_type = MessageType.LITERAL if int(data[3:6], 2) == 4 else MessageType.OPERATOR
    print('{}{} v{}:\n{}{} {} {}'.format(
        '\t'*DEPTH,
        msg_type.name,
        version,
        '\t'*DEPTH,
        data[0:3],
        data[3:6],
        data[6:]
    ))

    if msg_type == MessageType.LITERAL:
        value, end_index = parse_literal(data[6::])
        return [(version, msg_type, value, end_index)]
    else:
        sub_messages = parse_operator(data[6::])
        messages = [(version, msg_type, -1, -1)] + sub_messages
        return messages

def pt_1(data: list) -> int:
    messages = parse(data)
    print(messages)
    return sum(m[0] for m in messages)

def pt_2(data: list) -> int:
    pass

if __name__ == '__main__':
    data = load_data('demo.txt')
    for line in data:
        print(bin2hex(line))
        print(line, '\n')
        print(pt_1(line))
    print(pt_2(data))