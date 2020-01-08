from piece import CELL_FULL
import plotly.graph_objects as go
import plotly
import os
import time
import uuid


class SuperPiece:
    timestamp = time.time()
    plotly_directory_pieces = r'resources\super_pieces\{}'.format(timestamp)
    try:
        os.mkdir(plotly_directory_pieces)
    except OSError:
        print("Creation of the directory {} failed!".format(plotly_directory_pieces))

    def __init__(self, pieces):
        self.pieces = pieces
        self.max_axis_length = max([piece.max_axis_length for piece in self.pieces])

        self.id = uuid.uuid4()

        self.plotly_filename = \
            '{}_{}.html'.format('piece_{0:02d}_{0:02d}_{0:02d}'
                                .format(len(self.pieces), self.max_axis_length, self.max_axis_length), self.id)

    def output_piece_plotly(self):
        fig = go.Figure()
        location = os.path.join(self.plotly_directory_pieces, self.plotly_filename)

        for i, piece in enumerate(self.pieces):
            for xx in range(self.max_axis_length):
                for yy in range(self.max_axis_length):
                    if xx < piece.n and yy < piece.m:
                        if piece.matrix[yy][xx] == CELL_FULL:
                            fig.add_trace(go.Mesh3d(
                                x=piece.cube.x + xx,
                                y=piece.cube.y + yy,
                                z=piece.cube.z + i,
                                i=piece.cube.i,
                                j=piece.cube.j,
                                k=piece.cube.k,
                                name='cube'
                            ))
                    else:
                        fig.add_trace(go.Mesh3d(
                            x=piece.cube.x + xx,
                            y=piece.cube.y + yy,
                            z=piece.cube.z + i,
                            i=piece.cube.i,
                            j=piece.cube.j,
                            k=piece.cube.k,
                            name='cube_transparent',
                            opacity=0
                        ))

        plotly.offline.plot(fig, filename=location, auto_open=False)
