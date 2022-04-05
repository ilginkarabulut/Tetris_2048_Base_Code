import random


class Options:
    Options = int
    Options = [
        [ [0, 1, 4, 5], [2, 4, 5, 7], [1, 3, 4, 6], [3, 4, 7, 8], [0, 1, 2, 3]
                [1, 5, 9, 13], [4, 5, 6, 7], [2, 6, 10, 14], [8, 9, 10, 11],
                [1, 4, 7, 8], [3, 4, 5, 6], [0, 1, 4, 7], [2, 3, 4, 5],
                [1, 4, 6, 7], [0, 3, 4, 5], [1, 2, 4, 7], [3, 4, 5, 8],
                [1, 2, 3, 4], [1, 4, 5, 8], [4, 5, 6, 7], [0, 3, 4, 7],
                [1, 3, 4, 7], [1, 4, 5, 7], [3, 4, 5, 7], [1, 3, 4, 5] ],
        ]

    def __init__(self, x, y, colors=None):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.Options) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.Options[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.Options[self.type])