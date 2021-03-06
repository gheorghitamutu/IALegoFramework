from flask import Flask, Blueprint, redirect, url_for, render_template, request, json, jsonify
from werkzeug.utils import secure_filename
from threading import Thread
import os
from configuration import CommonConfigurations, Configuration
from piece import CommonPieces, Piece

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

user_made_pieces_bp = Blueprint(
    'user_made_pieces',
    __name__,
    static_folder='static',
    template_folder=os.path.join('web', 'templates', 'public', 'resources', 'pieces', 'user_made'))

user_made_configurations_bp = Blueprint(
    'user_made_configurations',
    __name__,
    static_folder='static',
    template_folder=os.path.join('web', 'templates', 'public', 'resources', 'configurations', 'user_made'))

app = Flask(__name__,
            static_url_path='',
            static_folder=os.path.join('web', 'static'),
            template_folder=os.path.join('web', 'templates', 'public'))


@app.route('/')
def index():
    return render_template('index.html')


def get_file_names_only(folder):
    path = os.path.join(app.template_folder, 'resources', folder)
    return [os.path.splitext(f.name)[0] for f in os.scandir(path) if os.path.isfile(f.path)]


@app.route('/configurations')
def configurations():
    return render_template('configurations.html', configurations=get_file_names_only('configurations'),
                           user_made_configurations=list(set(get_file_names_only('configurations\\user_made'))))


@configurations_bp.route('/configurations/<path:path>')
def render_configuration_file(path):
    return render_template(os.path.join('{}.html'.format(path)))


@app.route('/pieces')
def pieces():
    return render_template('pieces.html', pieces=get_file_names_only('pieces'),
                           user_made_pieces=list(set(get_file_names_only('pieces\\user_made'))))  # ignore json files


@pieces_bp.route('/pieces/<path:path>')
def render_piece_file(path):
    piece_template_name = os.path.join('{}.html'.format(path))
    piece_path = os.path.join(app.root_path, pieces_bp.template_folder, piece_template_name)
    if os.path.exists(piece_path):
        return render_template(piece_template_name)

    return redirect(url_for('user_made_pieces.render_user_piece_file', path=path))


@user_made_pieces_bp.route('/pieces/user_made/<path:path>')
def render_user_piece_file(path):
    piece_template_name = os.path.join('{}.html'.format(path))
    return render_template(piece_template_name)


def try_delete(files):
    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(e)


@app.route('/remove/pieces/<path:path>')
def remove_user_made_piece_files(path):
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
        filled_cells = [(x // size[1], x % size[1]) for x in filled_cells]
        size = [size[0], size[1]]

    user_made = True
    name = request.form['name']

    print(filled_cells)

    piece = Piece(
        size=size, filled_cells=filled_cells, fill_all=fill_all, name=name, user_made=user_made)
    piece.serialize()

    Thread(target=piece.output_piece_plotly()).start()  # drawing the SVG using plotly takes a lot

    return redirect(url_for('pieces'))


@app.route('/add/configurations')
def add_configurations():
    default_pieces = get_file_names_only('pieces')
    user_made_pieces = list(set(get_file_names_only('pieces\\user_made')))

    all_pieces_available = list()
    all_pieces_available.extend(default_pieces)
    all_pieces_available.extend(user_made_pieces)

    return render_template('add_configuration.html', pieces=all_pieces_available)


@app.route('/add/configuration', methods=['POST'])
def add_configuration():
    print(request.form)

    user_made = True
    name = request.form['name']
    pieces_names = request.form['selected_pieces'].split(',')
    height = request.form['height']  # not relevant

    configuration = Configuration(name=name, pieces=None, user_made=user_made, pieces_names=pieces_names)
    configuration.serialize()
    Thread(target=configuration.output_piece_plotly()).start()  # drawing the SVG using plotly takes a lot

    return redirect(url_for('configurations'))


@app.route('/remove/configurations/<path:path>')
def remove_user_made_configurations_files(path):
    files_to_delete = list()
    files_to_delete.append(
        '{}\\{}\\resources\\configurations\\user_made\\{}.html'.format(app.root_path, app.template_folder, path))
    files_to_delete.append(
        '{}\\{}\\resources\\configurations\\user_made\\{}.json'.format(app.root_path, app.template_folder, path))

    try_delete(files_to_delete)

    return redirect(url_for('configurations'))


@app.route('/custom_configuration')
def custom_configuration():
    return render_template('custom_configuration.html')


@user_made_configurations_bp.route('/configurations/user_made/<path:path>')
def render_user_configuration_file(path):
    configuration_template_name = os.path.join('{}.html'.format(path))
    return render_template(configuration_template_name)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['json']


@app.route('/custom_configuration/upload_result', methods=['POST'])
def configuration_upload():
    data = dict()
    file_path = ''

    file = request.files['upload_file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        data = {'success': False,
                'supported': False,
                'message': 'No selected file!'}
    elif file and allowed_file(file.filename):  # json only
        filename = secure_filename(file.filename)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    else:
        data = {'success': False,
                'supported': False,
                'message': 'File type not allowed!'}

    supported = True

    if file_path != '':
        with open(file_path, 'r') as f:
            json_object = json.load(f)

            if 'matrix-3d' in json_object:
                matrix_3d = json_object['matrix-3d']

                for matrix in matrix_3d:
                    matrix_supported = False

                    for name, piece in CommonPieces.items():
                        if matrix == piece.matrix:
                            matrix_supported = True
                            break

                    if not matrix_supported:

                        """
                            TODO: check user made pieces?
                        """

                        supported = False
                        break
            else:
                supported = False
    else:
        supported = False

    if len(data) == 0:
        data = {'success': True,
                'supported': supported,
                'message': ''}
    return jsonify(data)


def init_components():
    # make sure that all configurations are built
    for name, configuration in CommonConfigurations.items():
        configuration.output_piece_plotly()
        print('Created file for configuration {}.'.format(configuration.plotly_filename))

    user_made_configuration_folder = '{}\\{}\\resources\\configurations\\user_made'.format(
        app.root_path, app.template_folder)
    json_files = get_file_names_only(user_made_configuration_folder)
    for filename in json_files:
        full_path = '{}.json'.format(os.path.join(user_made_configuration_folder, filename))
        with open(full_path) as f:
            data = json.load(f)
            user_made = True
            name = data['name']
            pieces_names = data['pieces']

            configuration = Configuration(name=name, pieces=None, user_made=user_made, pieces_names=pieces_names)
            configuration.output_piece_plotly()

    # make sure that all pieces are built
    for name, piece in CommonPieces.items():
        piece.output_piece_plotly()
        print('Created file for piece {}.'.format(piece.plotly_filename))

    user_made_pieces_folder = '{}\\{}\\resources\\pieces\\user_made'.format(app.root_path, app.template_folder)
    json_files = get_file_names_only(user_made_pieces_folder)
    for filename in json_files:
        full_path = '{}.json'.format(os.path.join(user_made_pieces_folder, filename))
        with open(full_path) as f:
            data = json.load(f)
            size = None
            matrix = data['matrix']
            user_made = True
            name = data['name']

            piece = Piece(
                size=size, filled_cells=None, fill_all=False, name=name, user_made=user_made, matrix=matrix)
            piece.output_piece_plotly()


if __name__ == '__main__':
    thread = Thread(target=init_components)
    thread.start()

    app.config['UPLOAD_FOLDER'] = os.path.join('web', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16  -> raises RequestEntityTooLarge exception

    app.register_blueprint(pieces_bp)
    app.register_blueprint(configurations_bp)
    app.register_blueprint(user_made_pieces_bp)
    app.register_blueprint(user_made_configurations_bp)
    app.run(debug=True)
