import plotly.graph_objects as go
import plotly
import os
import uuid
import time
from cube import Cube
import json
import random

CELL_EMPTY = 0
CELL_FULL = 1


class Piece:
    def __init__(self, size, filled_cells=None, fill_all=False, name=None, user_made=False, matrix=None):
        self.user_made = user_made

        if matrix is None:
            self.n = size[0]
            self.m = size[1]
            self.matrix = [[CELL_FULL if fill_all else CELL_EMPTY] * self.m for _ in range(self.n)]
        else:
            self.n = len(matrix)
            self.m = len(matrix[0])
            self.matrix = matrix

        self.cube = Cube()

        self.id = uuid.uuid4()

        self.plotly_directory_pieces = r'web\templates\public\resources\pieces'
        try:
            if os.path.exists(self.plotly_directory_pieces) is False:
                os.mkdir(self.plotly_directory_pieces)
        except OSError:
            print("Creation of the directory {} failed!".format(self.plotly_directory_pieces))

        self.serialize_folder = r'{}\user_made'.format(self.plotly_directory_pieces)
        try:
            if os.path.exists(self.serialize_folder) is False:
                os.mkdir(self.serialize_folder)
        except OSError:
            print("Creation of the directory {} failed!".format(self.serialize_folder))

        if user_made is True:
            self.plotly_directory_pieces = '{}\\user_made'.format(self.plotly_directory_pieces)

        if name is None:
            self.plotly_directory_pieces = r'{}\{}'.format(self.plotly_directory_pieces, time.time())
            self.plotly_filename = '{}_{}.html'.format('piece_{0:02d}_{0:02d}'.format(self.n, self.m), self.id)
        else:
            self.plotly_filename = name if name[:-5] == '.html' and len(name) > 5 else '{}.html'.format(name)

        if fill_all is False and filled_cells is not None:
            for i in filled_cells:
                try:
                    x = i[0]
                    y = i[1]

                    self.matrix[x][y] = CELL_FULL
                except IndexError as e:
                    print('ERROR: x {} y {} n {} m {}'.format(i[0], i[1], self.n, self.m))

        self.max_axis_length = max(self.n, self.m)

    def output_matrix(self):
        for i in self.matrix:
            for j in i:
                print("{} ".format(j), end="")
            print()

    def output_piece_plotly(self):
        fig = go.Figure()
        location = os.path.join(self.plotly_directory_pieces, self.plotly_filename)

        color_index = random.randint(0, len(plotly.colors.DEFAULT_PLOTLY_COLORS) - 1)
        color = plotly.colors.DEFAULT_PLOTLY_COLORS[color_index]

        for xx in range(self.n):
            for yy in range(self.m):
                if xx < self.n and yy < self.m:
                    try:
                        if self.matrix[xx][yy] == CELL_FULL:
                            fig.add_trace(go.Mesh3d(
                                x=self.cube.x + xx,
                                y=self.cube.y + yy,
                                z=self.cube.z,  # + zz,
                                i=self.cube.i,
                                j=self.cube.j,
                                k=self.cube.k,
                                name='cube',
                                color=color
                            ))

                        # fix the issue for one layer spanning too wide adding another transparent layer
                        fig.add_trace(go.Mesh3d(
                            x=self.cube.x + xx,
                            y=self.cube.y + yy,
                            z=self.cube.z + 1,  # + zz,
                            i=self.cube.i,
                            j=self.cube.j,
                            k=self.cube.k,
                            name='cube',
                            opacity=0
                        ))
                    except IndexError as e:
                        print('ERROR xx yy: x {} y {} n {} m {}'.format(xx, yy, self.n, self.m))

        plotly.offline.plot(fig, filename=location, auto_open=False)

    def serialize(self):
        original_piece_name = self.plotly_filename.replace('.html', '')

        json_data = {
            'name': original_piece_name,
            'matrix': self.matrix
        }

        json_filename = r'{}\{}.json'.format(self.serialize_folder, original_piece_name)
        with open(json_filename, 'w') as json_file:
            json.dump(json_data, json_file)


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
        name='66_border'),

    '77_full': Piece(
        (7, 7),
        fill_all=True,
        name='77_full'),

    '77_as_55': Piece(
        (7, 7),
        [
            (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
            (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
            (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
            (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)
        ],
        name='77_as_55'),

    '77_as_33': Piece(
        (7, 7),
        [
            (2, 2), (2, 3), (2, 4),
            (3, 2), (3, 3), (3, 4),
            (4, 2), (4, 3), (4, 4),
        ],
        name='77_as_33'),

    '77_as_11': Piece(
        (7, 7),
        [
            (3, 3)
        ],
        name='77_as_11'),

    '77_double_border': Piece(  # yes, there are some duplicates
        (7, 7),
        [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),

            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
            (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),

            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
            (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5),

            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
            (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6)
        ],
        name='77_double_border'),

    '77_border_without_middle': Piece(
        (7, 7),
        [
            (0, 0), (0, 1), (0, 5), (0, 6),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
            (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6)
        ],
        name='77_border_without_middle'),

    '77_border': Piece(
        (7, 7),
        [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
            (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6)
        ],
        name='77_border'),

    '77_as_66_double_border': Piece(  # yes, there are some duplicates
        (7, 7),
        [
            (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
            (2, 1), (3, 1), (4, 1), (5, 1),

            (2, 1), (2, 2), (2, 3), (1, 4), (2, 5),
            (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),

            (4, 1), (4, 2), (4, 3), (4, 4),
            (1, 4), (2, 4), (3, 4), (4, 4),

            (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
            (2, 5), (3, 5), (4, 5), (5, 5)
        ],
        name='77_as_66_double_border'),
}
