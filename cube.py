import numpy as np


class Cube:
    def __init__(self):
        self.x = np.array([0, 0, 1, 1, 0, 0, 1, 1])
        self.y = np.array([0, 1, 1, 0, 0, 1, 1, 0])
        self.z = np.array([0, 0, 0, 0, 1, 1, 1, 1])

        self.i = np.array([7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2])
        self.j = np.array([3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3])
        self.k = np.array([0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6])
