import plotly.graph_objects as go
import plotly
import os
import uuid
import time
from cube import Cube

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
        self.cube = Cube()

        self.id = uuid.uuid4()

        self.plotly_filename = '{}_{}.html'.format('piece_{0:02d}_{0:02d}'.format(self.n, self.m), self.id)

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
