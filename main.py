from flask import Flask, Blueprint, redirect, url_for
from flask import render_template
import os
from configuration import CommonConfigurations
from piece import CommonPieces, Piece
from threading import Thread
from flask import request

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
    return [os.path.splitext(f.name)[0] for f in os.scandir(path) if os.path.isfile(f.path)]


@app.route('/configurations')
def configurations():
    return render_template('configurations.html', configurations=get_files_list_from('configurations'),
                           user_made_configurations=get_files_list_from('configurations\\user_made'))


@configurations_bp.route('/configurations/<path:path>')
def render_configuration_file(path):
    return render_template(os.path.join('{}.html'.format(path)))


@app.route('/pieces')
def pieces():
    return render_template('pieces.html', pieces=get_files_list_from('pieces'),
                           user_made_pieces=get_files_list_from('pieces\\user_made'))


@pieces_bp.route('/pieces/<path:path>')
def render_piece_file(path):
    return render_template(os.path.join('{}.html'.format(path)))


def try_delete(files):
    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(e)


@app.route('/remove/pieces/<path:path>')
def render_piece_file(path):
    files_to_delete = list()
    files_to_delete.append(
        '{}\\{}\\resources\\pieces\\user_made\\{}.html'.format(app.root_path, app.template_folder, path))
    files_to_delete.append(
        '{}\\{}\\resources\\pieces\\user_made\\{}.json'.format(app.root_path, app.template_folder, path))

    try_delete(files_to_delete)

    return redirect(url_for('pieces'))


@app.route('/add/pieces')
def add_pieces():
    return render_template('add_piece.html')


@app.route('/add/piece', methods=['POST'])
def add_piece():
    print(request.form)

    size = [int(request.form['height']), int(request.form['width'])]
    filled_cells = [int(x) for x in request.form['selected_cells'].split(',')]
    fill_all = False

    if len(filled_cells) == size[0] * size[1]:
        fill_all = True
        filled_cells = None
    else:
        filled_cells = [(x // size[0], x % size[0]) for x in filled_cells]
        size = [size[1], size[0]]  # TODO: check why these are inverted in piece

    user_made = True
    name = request.form['name']

    print(filled_cells)

    piece = Piece(size=size, filled_cells=filled_cells, fill_all=fill_all, name=name, user_made=user_made)
    piece.serialize()

    return redirect(url_for('pieces'))


def init_components():
    # make sure default CommonConfiguration are built
    for name, configuration in CommonConfigurations.items():
        configuration.output_piece_plotly()
        print('Created file for configuration {}.'.format(configuration.plotly_filename))
        configuration.serialize()
        print('Serialized configuration {}.'.format(configuration.plotly_filename))

    # make sure default CommonPieces are built
    for name, piece in CommonPieces.items():
        piece.output_piece_plotly()
        print('Created file for piece {}.'.format(piece.plotly_filename))


if __name__ == '__main__':
    thread = Thread(target=init_components)
    thread.start()

    app.register_blueprint(pieces_bp)
    app.register_blueprint(configurations_bp)
    app.run(debug=True)
