class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def diagonal(self):
        return self.x1 != self.x2 and self.y1 != self.y2

    @property
    def bbox(self):
        return (min(self.x1, self.x2), min(self.y1, self.y2), max(self.x1, self.x2), max(self.y1, self.y2))

    @property
    def bresenham(self):
        # https://en.wikipedia.org/wiki/Bresenham's_line_algorithm
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        xsign = 1 if dx>0 else -1
        ysign = 1 if dy>0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2*dy - dx
        y = 0

        for x in range(dx + 1):
            yield self.x1 + x*xx + y*yx, self.y1 + x*xy + y*yy
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy

    def __repr__(self):
        return f'Line({self.x1},{self.y1} -> {self.x2},{self.y2}), diag={self.diagonal}'

class Terrain:
    def __init__(self):
        self.lines = []
        self.bbox = None
        self.field = None

    def recalc(self):
        self.calc_bbox()
        self.calc_field()

    def calc_bbox(self):
        bboxes = [line.bbox for line in self.lines]
        self.bbox = (
            min([b[0] for b in bboxes]),
            min([b[1] for b in bboxes]),
            max([b[2] for b in bboxes]),
            max([b[3] for b in bboxes]),
        )

    def calc_field(self):
        self.field = [
            [0] * (self.bbox[3] - self.bbox[1] + 1)
            for _ in range(self.bbox[2] - self.bbox[0] + 1)
        ]
        for line in self.lines:
            for x, y in line.bresenham:
                self.field[y - self.bbox[0]][x - self.bbox[1]] += 1

    def add_lines(self, data):
        for coords in data:
            self.lines.append(Line(*coords))
        self.recalc()

    def discard_diagonal_lines(self):
        self.lines = [line for line in self.lines if not line.diagonal]
        self.recalc()

    @property
    def intersections(self):
        return [
            (x, y)
            for y in range(len(self.field))
            for x in range(len(self.field[y]))
            if self.field[y][x] > 1
        ]

    def __repr__(self):
        out_str = ''
        for row in range(len(self.field)):
            for col in range(len(self.field[row])):
                out_str += ('.' if self.field[row][col] == 0 else str(self.field[row][col])).ljust(2)
            out_str += '\n'
        return out_str

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        buffer = [i for i in f.readlines()]
        data = [
            [int(i) for i in line.replace(' -> ', ',').strip().split(',')]
            for line in buffer
        ]
    terrain = Terrain()
    terrain.add_lines(data)
    #terrain.discard_diagonal_lines()
    print(len(terrain.intersections))
