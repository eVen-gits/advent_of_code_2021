def bin_str(n: int, length: int) -> str:
    """
    Convert an integer to a binary string.
    """
    return format(n, 'b').zfill(length)

class Node:
    def __init__(self, bin_len):
        self.bin_len = bin_len
        self.count = 0
        if not bin_len:
            self.zero = None
            self.one = None
        else:
            self.zero = Node(bin_len-1)
            self.one = Node(bin_len-1)

    def process(self, num: int) -> None:
        self.count += 1
        if self.bin_len == 0:
            return
        bit = 1 if bool(num & (1 << self.bin_len)) else 0
        if bit:
            self.one.process(num)
        else:
            self.zero.process(num)

    def __repr__(self):
        return str(self.count)


if __name__ == '__main__':
    with open('demo.txt', 'r') as f:
        data = [i for i in f.readlines()]
        blen = len(data[0].strip())
        data = [int(i, 2) for i in data]

    root = Node(blen)
    for i in data:
        root.process(i)
    print(root.count)
