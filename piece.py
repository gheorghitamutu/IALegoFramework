import plotly.graph_objects as go
import plotly
import os
import uuid
import time
from cube import Cube

CELL_EMPTY = 0
CELL_FULL = 1


class Piece:
    plotly_directory_pieces = r'web\templates\public\resources\pieces'
    try:
        if os.path.exists(plotly_directory_pieces) is False:
            os.mkdir(plotly_directory_pieces)
    except OSError:
        print("Creation of the directory {} failed!".format(plotly_directory_pieces))

    def __init__(self, size, filled_cells=None, fill_all=False, name=None):
        self.n = size[0]
        self.m = size[1]
        self.matrix = [[CELL_FULL if fill_all else CELL_EMPTY] * self.n for _ in range(self.m)]
        self.cube = Cube()

        self.id = uuid.uuid4()

        if name is None:
            self.plotly_directory_pieces = r'{}\{}'.format(self.plotly_directory_pieces, time.time())
            self.plotly_filename = '{}_{}.html'.format('piece_{0:02d}_{0:02d}'.format(self.n, self.m), self.id)
        else:
            self.plotly_filename = name if name[:-5] == '.html' and len(name) > 5 else '{}.html'.format(name)

        if fill_all is False and filled_cells is not None:
            for i in filled_cells:
                self.matrix[i[0]][i[1]] = CELL_FULL

        self.max_axis_length = max(self.n, self.m)

    def output_matrix(self):
        for i in self.matrix:
            for j in i:
                print("{} ".format(j), end="")
            print()

    def output_piece_plotly(self):
        fig = go.Figure()
        location = os.path.join(self.plotly_directory_pieces, self.plotly_filename)

        for xx in range(self.max_axis_length):
            for yy in range(self.max_axis_length):
                for zz in range(self.max_axis_length):

                    if xx < self.n and yy < self.m and zz == 0:
                        if self.matrix[yy][xx] == CELL_FULL:
                            fig.add_trace(go.Mesh3d(
                                x=self.cube.x + xx,
                                y=self.cube.y + yy,
                                z=self.cube.z + zz,
                                i=self.cube.i,
                                j=self.cube.j,
                                k=self.cube.k,
                                name='cube'
                            ))
                    else:
                        fig.add_trace(go.Mesh3d(
                            x=self.cube.x + xx,
                            y=self.cube.y + yy,
                            z=self.cube.z + zz,
                            i=self.cube.i,
                            j=self.cube.j,
                            k=self.cube.k,
                            name='cube_transparent',
                            opacity=0
                        ))

        plotly.offline.plot(fig, filename=location, auto_open=False)


Random_Pieces = [
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

CommonPieces = {
    '66_full': Piece(
        (6, 6),
        fill_all=True,
        name='66_full'),

    '66_as_44': Piece(
        (6, 6),
        [
            (1, 1), (1, 2), (1, 3), (1, 4),
            (2, 1), (2, 2), (2, 3), (2, 4),
            (3, 1), (3, 2), (3, 3), (3, 4),
            (4, 1), (4, 2), (4, 3), (4, 4)
        ],
        name='66_as_44'),

    '66_as_22': Piece(
        (6, 6),
        [
            (2, 2), (2, 3),
            (3, 2), (3, 3)
        ],
        name='66_as_22'),

    '66_border': Piece(
        (6, 6),
        [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
            (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)
        ],
        name='66_border')
}