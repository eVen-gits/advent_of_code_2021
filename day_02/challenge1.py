from enum import Enum

class Command(Enum):
    FORWARD = 1
    DOWN = 2
    UP = 3

class State:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset to initial state"""
        self.position = 0
        self.depth = 0
        self.aim = 0

    def process(self, data, action_method):
        """
        Process the data and return the product of position and depth
        - data: list of commands
        - action_method: function to apply to each command
        """
        self.reset()
        for cmd, val in data:
            action_method(cmd, val)

        return self.position * self.depth

    def action_pt0(self, command: Command, value: int):
        if command == Command.FORWARD:
            self.position += value
        elif command == Command.DOWN:
            self.depth += value
        elif command == Command.UP:
            self.depth -= value
        else:
            raise ValueError(f"Invalid command: {command}")

    def action_pt1(self, command: Command, value: int):
        if command == Command.FORWARD:
            self.position += value
            self.depth += self.aim * value
        elif command == Command.DOWN:
            self.aim += value
        else:
            self.aim -= value

    def __repr__(self):
        return f"{self.position} {self.depth}"

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
            data = [i.split(' ') for i in f.readlines()]
            data = [(Command[d[0].upper()], int(d[1])) for d in data]

    state = State()
    print(state.process(data, state.action_pt0))
    print(state.process(data, state.action_pt1))