import plotly.graph_objects as go
import numpy as np
import plotly
import os
import uuid
import time

CELL_EMPTY = 0
CELL_FULL = 1


class Piece:
    timestamp = time.time()
    plotly_directory_pieces = r'resources\pieces\{}'.format(timestamp)
    try:
        os.mkdir(plotly_directory_pieces)
    except OSError:
        print("Creation of the directory {} failed!".format(plotly_directory_pieces))

    def __init__(self, size, filled_cells=None, fill_all=False):
        self.n = size[0]
        self.m = size[1]
        self.matrix = [[CELL_FULL if fill_all else CELL_EMPTY] * self.n for _ in range(self.m)]

        # plotly cube data
        self.x = np.array([0, 0, 1, 1, 0, 0, 1, 1])
        self.y = np.array([0, 1, 1, 0, 0, 1, 1, 0])
        self.z = np.array([0, 0, 0, 0, 1, 1, 1, 1])

        self.i = np.array([7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2])
        self.j = np.array([3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3])
        self.k = np.array([0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6])

        self.id = uuid.uuid4()

        self.plotly_filename = '{}_{}.html'.format('piece_{0:02d}_{0:02d}'.format(self.n, self.m), self.id)
        # end plotly cube data

        if fill_all is False and filled_cells is not None:
            for i in filled_cells:
                self.matrix[i[0]][i[1]] = CELL_FULL

    def output_matrix(self):
        for i in self.matrix:
            for j in i:
                print("{} ".format(j), end="")
            print()

    def output_piece_plotly(self):
        fig = go.Figure()
        location = os.path.join(self.plotly_directory_pieces, self.plotly_filename)

        max_axis_length = max(self.n, self.m)

        for xx in range(max_axis_length):
            for yy in range(max_axis_length):
                for zz in range(max_axis_length):

                    if xx < self.n and yy < self.m and zz == 0:
                        if self.matrix[yy][xx] == CELL_FULL:
                            fig.add_trace(go.Mesh3d(
                                x=self.x + xx,
                                y=self.y + yy,
                                z=self.z + zz,
                                i=self.i,
                                j=self.j,
                                k=self.k,
                                name='cube'
                            ))
                    else:
                        fig.add_trace(go.Mesh3d(
                            x=self.x + xx,
                            y=self.y + yy,
                            z=self.z + zz,
                            i=self.i,
                            j=self.j,
                            k=self.k,
                            name='cube_transparent',
                            opacity=0
                        ))

        plotly.offline.plot(fig, filename=location, auto_open=False)


piece_list = [
    Piece((2, 2), [(0, 0), (0, 1), (1, 0)]),
    Piece((12, 2), fill_all=True),
    Piece((2, 12), fill_all=True),
    Piece((2, 6), fill_all=True),
    Piece((6, 2), fill_all=True),
    Piece((1, 1), fill_all=True),
    Piece((1, 2), fill_all=True),
    Piece((2, 1), fill_all=True),
    Piece((1, 8), fill_all=True),
    Piece((8, 1), fill_all=True),

    Piece((3, 3), [(0, 0), (0, 1), (1, 0), (2, 0), (1, 1), (2, 1), (2, 2)]),
    Piece((2, 2), [(0, 0), (0, 1), (1, 1)]),
    Piece((3, 3), [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2)]),
    Piece((3, 3), [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (1, 2), (2, 2)]),
    Piece((3, 4), fill_all=True),
    Piece((3, 1), fill_all=True),
    Piece((1, 3), fill_all=True),
    Piece((4, 3), fill_all=True),
    Piece((2, 2), fill_all=True),
    Piece((5, 2), fill_all=True)
]

for piece in piece_list:
    piece.output_matrix()
    print()
    piece.output_piece_plotly()

