import sys

DEBUG = False

def load_data(filename):
    with open(filename, 'r') as f:
        data = [line.strip() for line in f.readlines()]
    return data


class CaveSystem:
    def __init__(self):
        self.nodes = {}
        self.paths = []

    @property
    def start(self):
        return self.nodes['start']

    @property
    def end(self):
        return self.nodes['end']

    def parse_data(self, data):
        for line in data:
            n1, n2 = line.split('-')
            if not n1 in self.nodes:
                self.nodes[n1] = Node(n1)
            if not n2 in self.nodes:
                self.nodes[n2] = Node(n2)
            self.nodes[n1].neighbors.add(n2)
            self.nodes[n2].neighbors.add(n1)

    def explore_pt1(self):
        queue = [[self.start.name]]
        while queue:
            path = queue.pop(0)

            node = self.nodes[path[-1]]
            if node == self.end:
                self.paths.append(path)
                continue
            for neighbour in node.neighbors:
                if neighbour.isupper() or neighbour not in path:
                    queue.append(path+[neighbour])
        if DEBUG: [print(','.join(path)) for path in self.paths]
        return self.paths

    def explore_pt2(self):
        queue = [([self.start.name], True)]
        while queue:
            if DEBUG:
                sys.stdout.write("Queue size: %d\r" % (len(queue)) )
                sys.stdout.flush()
            path, dup_ok = queue.pop(0)
            node = self.nodes[path[-1]]
            for neighbor in node.neighbors:
                if neighbor == 'end':
                    self.paths.append(path + [neighbor])
                elif neighbor == 'start':
                    continue
                elif neighbor.isupper() or neighbor not in path:
                    queue.append((path+[neighbor], dup_ok))
                elif dup_ok:
                    queue.append((path + [neighbor], False))
        if DEBUG: [print(','.join(path)) for path in self.paths]
        return self.paths

    def __repr__(self) -> str:
        return '\n'.join([
            '->'.join([n.name for n in path])
            for path in self.paths
        ])

class Node:
    def __init__(self, name):
        self.name = name
        self.large = name.isupper()
        self.neighbors = set()

    def __repr__(self):
        return '<Node {}>({})'.format(
            self.name,
            '->'.join([n.name for n in self.path]),
            ', '.join([n.name for n in self.neighbors]),
        )

def pt_1(data):
    system = CaveSystem()
    system.parse_data(data)
    return len(system.explore_pt1())

def pt_2(data):
    system = CaveSystem()
    system.parse_data(data)
    return len(system.explore_pt2())

if __name__ == '__main__':
    data = load_data('input.txt')
    print(pt_1(data))
    print(pt_2(data))