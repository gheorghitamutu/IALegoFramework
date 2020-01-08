from flask import Flask, Blueprint
from flask import render_template
import os
from configuration import CommonConfigurations
from piece import CommonPieces

configurations_bp = Blueprint(
    'configurations',
    __name__,
    static_folder='static',
    template_folder=os.path.join('web', 'templates', 'public', 'resources', 'configurations'))

pieces_bp = Blueprint(
    'pieces',
    __name__,
    static_folder='static',
    template_folder=os.path.join('web', 'templates', 'public', 'resources', 'pieces'))


app = Flask(__name__,
            static_url_path='',
            static_folder=os.path.join('web', 'static'),
            template_folder=os.path.join('web', 'templates', 'public'))


@app.route('/')
def index():
    return render_template('index.html', message='test')


def get_files_list_from(folder):
    path = os.path.join(app.template_folder, 'resources', folder)
    return [f.name.replace('.html', '') for f in os.scandir(path) if os.path.isfile(f.path)]


@app.route('/configurations')
def configurations():
    return render_template('configurations.html', configurations=get_files_list_from('configurations'))


@configurations_bp.route('/configurations/<path:path>')
def render_configuration_file(path):
    return render_template(os.path.join('{}.html'.format(path)))


@app.route('/pieces')
def pieces():
    return render_template('pieces.html', pieces=get_files_list_from('pieces'))


@pieces_bp.route('/pieces/<path:path>')
def render_piece_file(path):
    return render_template(os.path.join('{}.html'.format(path)))


if __name__ == '__main__':
    # make sure default CommonConfiguration are built
    for name, configuration in CommonConfigurations.items():
        configuration.output_piece_plotly()

    # make sure default CommonPieces are built
    for name, piece in CommonPieces.items():
        piece.output_piece_plotly()

    app.register_blueprint(pieces_bp)
    app.register_blueprint(configurations_bp)
    app.run(debug=True)
