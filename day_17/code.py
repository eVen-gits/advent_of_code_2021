from tqdm import tqdm
from math import sqrt
DEBUG = False

### PROOFING FUNCTIONS
def calc_y(y_speed):
    # Vertical speed at max y is 0
    # Vertical speed at 0 is -(initial_speed+1)
    ys = []
    y = 0
    while y >= 0:
        ys.append(y)
        y += y_speed
        y_speed -= 1
    return ys

def speed_at_step(starting, step):
    # speed at horizontal vertical line is going to be -(starting+1)
    return starting - step

def max_y(y_speed):
    #The following part is equal
    #you can get sum of sequence directly
    #Vertical speed is 0 at max y

    #return sum(range(y_speed+1))
    return y_speed * (y_speed + 1) // 2

def steps_to_zero(speed):
    # steps of -1 to reach speed = 0 is (speed+1)
    # steps of -1 to reach y = 0 is twiche as much
    return speed * 2 + 2


### SOLTUION

def load_data(filename):
    with open(filename, 'r') as f:
        data = [
            [
                int(v.replace(',', ''))
                for v
                in p[2:].split('..')
            ]
            for p in
            f.readline().split(' ')[2:]
        ]
    return (data[0][0], data[0][1], data[1][0], data[1][1])

def print_area(limits, trajectory=[]):
    xmin, xmax, ymin, ymax = limits

    steps_xmin = min([t[0] for t in trajectory])
    steps_ymin = min([t[1] for t in trajectory])

    steps_xmax = max([t[0] for t in trajectory])
    steps_ymax = max([t[1] for t in trajectory])

    box_xmin = min([xmin, xmax, 0, steps_xmin])
    box_xmax = max([xmin, xmax, 0, steps_xmax])

    box_ymin = min([ymin, ymax, 0, steps_ymin])
    box_ymax = max([ymin, ymax, 0, steps_ymax])

    for y in range(box_ymax, box_ymin - 1, -1):
        for x in range(box_xmin, box_xmax+1):
            if x == y == 0:
                print('S', end='')
            elif (x, y) in trajectory:
                print('#', end='')
            elif all([
                ymin <= y <= ymax,
                xmin <= x <= xmax,
            ]):
                print('T', end='')
            else:
                print('.', end='')
        print()

def calculate_path_explicitly(x, y, limits):
    xmin, xmax, ymin, ymax = limits
    steps = [(0, 0)]
    while True:
        nx = steps[-1][0] + x
        ny =steps[-1][1] + y
        if nx > xmax or ny < ymin:
            break
        steps.append((nx, ny))
        if x < 0:
            x += 1
        elif x > 0:
            x -= 1
        y -= 1

    return steps

def test(dx, dy, limits):
    xmin, xmax, ymin, ymax = limits
    x, y = 0, 0
    while y >= ymin:
        x,y = x+dx, y+dy
        dx += (dx<=0)-(dx>=0) # move dx closer to 0
        dy -= 1
        if x in range(xmin, xmax+1):
            if y in range(ymin,ymax+1):
                return 1
        elif dx==0:
            break
    return 0

def calc_x(dist):
    D = sqrt(1/4 + 2*dist)
    x1 = -0.5 + D
    x2 = -0.5 - D
    # apparently, this is faster than max()
    return int(x1 if x1 > x2 else x2)

def calc_valid_speeds(limits):
    xmin, xmax, *_ = limits
    vxmin = calc_x(xmin)
    speeds = []
    for v0 in range(vxmin, xmax):
        px = 0
        vx = v0
        while px < xmax+1:
            px += vx
            vx -= 1
            if vx < 1:
                break
            if px in range(xmin, xmax+1):
                speeds.append(vx)
    return set(speeds)

def pt_1(data) -> int:
    xmin, xmax, ymin, ymax = data
    return ymin*(ymin+1)//2

def pt_2(data) -> int:
    xmin, xmax, ymin, ymax = data
    x_range = calc_x(xmin), calc_x(xmax)
    #TODO: Calculate upper bound for X speed
    # this depends on whether we are sling shoting (arc)
    # or shooting directly (straight)

    # dy and dy are connected - have to figure out which one should be considered first

    #TODO: This doesnt seem to be working properly
    #x_speeds = calc_valid_speeds(data)

    vals = [
        test(dx, dy, data)
        for dx in range(x_range[0], xmax+1)
        for dy in range(ymin, 1-ymin)
    ]
    return sum(vals)

if __name__ == '__main__':
    data = load_data('demo.txt')
    print(pt_1(data))
    print(pt_2(data))
