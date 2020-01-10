from piece import CommonPieces, CELL_FULL
import plotly.graph_objects as go
import plotly
import os
import time
import uuid
import json


class Configuration:
    plotly_directory_configurations = r'web\templates\public\resources\configurations'
    try:
        if os.path.exists(plotly_directory_configurations) is False:
            os.mkdir(plotly_directory_configurations)
    except OSError:
        print("Creation of the directory {} failed!".format(plotly_directory_configurations))

    serialize_folder = r'{}\user_made'.format(plotly_directory_configurations)
    try:
        if os.path.exists(serialize_folder) is False:
            os.mkdir(serialize_folder)
    except OSError:
        print("Creation of the directory {} failed!".format(serialize_folder))

    def __init__(self, pieces, name=None):
        self.user_made = False

        self.pieces = pieces
        self.max_axis_length = max([piece.max_axis_length for piece in self.pieces])

        self.id = uuid.uuid4()

        if name is None:
            self.plotly_directory_configurations = r'{}\{}'.format(self.plotly_directory_configurations, time.time())
            self.plotly_filename = \
                '{}_{}.html'.format('configuration_{0:02d}_{0:02d}_{0:02d}'
                                    .format(len(self.pieces), self.max_axis_length, self.max_axis_length), self.id)
        else:
            self.plotly_filename = name if name[:-5] == '.html' and len(name) > 5 else '{}.html'.format(name)

    def output_piece_plotly(self):
        fig = go.Figure()
        location = os.path.join(self.plotly_directory_configurations, self.plotly_filename)

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

    def serialize(self):
        original_configuration_name = self.plotly_filename.replace('.html', '')

        json_data = {
            'name': original_configuration_name,
            'pieces': [piece.plotly_filename.replace('.html', '') for piece in self.pieces]
        }

        json_filename = r'{}\{}.json'.format(self.serialize_folder, original_configuration_name)
        with open(json_filename, 'w') as json_file:
            json.dump(json_data, json_file)


CommonConfigurations = {
    'pyramid': Configuration(
        pieces=[
            CommonPieces['66_full'],
            CommonPieces['66_as_44'],
            CommonPieces['66_as_22']
        ],
        name='pyramid'
    ),

    '3_sided_cube': Configuration(
        pieces=[
            CommonPieces['66_full'],
            CommonPieces['66_border'],
            CommonPieces['66_border'],
            CommonPieces['66_border'],
            CommonPieces['66_border']
        ],
        name='3_sided_cube'
    ),

    'sphere': Configuration(
        pieces=[
            CommonPieces['77_as_11'],
            CommonPieces['77_as_33'],
            CommonPieces['77_as_55'],
            CommonPieces['77_full'],
            CommonPieces['77_as_55'],
            CommonPieces['77_as_33'],
            CommonPieces['77_as_11']
        ],
        name='sphere'
    ),

    'home': Configuration(
        pieces=[
            CommonPieces['77_full'],
            CommonPieces['77_border_without_middle'],
            CommonPieces['77_border_without_middle'],
            CommonPieces['77_border_without_middle'],
            CommonPieces['77_border_without_middle'],
            CommonPieces['77_border'],
            CommonPieces['77_border'],
            CommonPieces['77_double_border'],
            CommonPieces['77_as_66_double_border'],
            CommonPieces['77_as_33'],
            CommonPieces['77_as_11']
        ],
        name='home'
    )
}
