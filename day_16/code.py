import sys
from enum import Enum

class MessageType(Enum):
    OPERATOR = 0
    LITERAL = 4

class OperatorType(Enum):
    IMMEDIATE = 4
    NESTED = 0

DEBUG = False
DEPTH = 0

class Packet:
    def __init__(self, version, type):
        self.version = version
        self.packet_type = type
        self.content_size = None
        self._data = None
        '''self.packet_type = (
            MessageType.LITERAL
            if int(data[3:6], 2) == 4
            else MessageType.OPERATOR
        )
        self.data = data[6:]'''

    @property
    def subpackets(self):
        subpackets = [self]
        if self.packet_type == MessageType.OPERATOR:
            for packet in self.packets:
                subpackets += packet.subpackets
        return subpackets

    @staticmethod
    def parse(data):
        version = int(data[0:3], 2)
        packet_type = (
            MessageType.LITERAL
            if int(data[3:6], 2) == 4
            else MessageType.OPERATOR
        )

        if packet_type == MessageType.LITERAL:
            packet = LiteralPacket(version)
        else:
            packet = OperatorPacket(version)
        #print(packet_type.name, version)
        packet.parse(data)
        packet._data = data[:packet.size]
        print(packet)
        return packet

    def __repr__(self):
        return '<Packet version={} type={}> {}'.format(self.version, self.packet_type, self.data_str)

class LiteralPacket(Packet):
    def __init__(self, version):
        Packet.__init__(self, version, MessageType.LITERAL)

    @property
    def size(self):
        return self.content_size + 6

    def parse(self, data):
        self._data = data
        idx = 6
        field = data[idx:idx+5]
        number = ''
        while True:
            number += field[1::]
            idx += 5
            if field[0] == '0':
                break
            field = data[idx:idx+5]

        self.value = int(number, 2)
        self.content_size = idx - 6
        return None

    @property
    def data_str(self):
        #return '{}'.format(self._data[0:self.content_size])
        return '{} {} {}'.format(
            self._data[0:3],
            self._data[3:6],
            self._data[6:6+self.content_size]
        )

    def __repr__(self):
        return '<LiteralPacket version={} value={} size={}> {}'.format(
            self.version, self.value, self.size, self.data_str
        )

class OperatorPacket(Packet):
    def __init__(self, version):
        Packet.__init__(self, version, MessageType.OPERATOR)
        self.operator_type = None
        self.packets = []

    @property
    def size(self):
        return 18 + self.operator_type.value + sum(packet.size for packet in self.packets)

    #overwrite
    def parse(self, data):
        global DEPTH
        self._data = data

        self.operator_type = (
            OperatorType.NESTED
            if data[6] == '0'
            else OperatorType.IMMEDIATE
        )

        if self.operator_type == OperatorType.NESTED:
            subpackets_size = int(data[7:22], 2)
            idx = 22
            DEPTH += 1
            while idx < subpackets_size + 22:
                packet = Packet.parse(data[idx:])
                self.packets.append(packet)
                idx += packet.size
            DEPTH -= 1
            return self
        else:
            n_subpackets = int(data[7:18], 2)
            idx = 18
            for _ in range(n_subpackets):
                packet = Packet.parse(data[idx:])
                self.packets.append(packet)
                idx += packet.size
            return self

    @property
    def data_str(self):
        return '{} {} {} {} ({})'.format(
            self._data[0:3],
            self._data[3:6],
            self._data[6],
            self._data[7:19+self.operator_type.value],
            ' '.join(packet.data_str for packet in self.packets)
        )

    def __repr__(self):
        return '<OperatorPacket version={} type={} packets={} size={}> {}\n\t{}'.format(
            self.version, self.operator_type.name, len(self.packets), self.size,
            self.data_str,
            '\n\t'.join([str(p) for p in self.packets])
        )

        #return '<OperatorPacket version={} type={}>'.format(self.version, self.operator_type)


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

def pt_1(data: list) -> int:
    packet = Packet.parse(data)
    print([p.version for p in packet.subpackets])
    #print(messages)
    #return sum(m[0] for m in messages)

def pt_2(data: list) -> int:
    pass

if __name__ == '__main__':
    #for i in range(7):
    data = load_data('demo_{}.txt'.format(4))
    for line in data:
        print(bin2hex(line))
        print(line, '\n')
        print(pt_1(line))
    #print(pt_2(data))