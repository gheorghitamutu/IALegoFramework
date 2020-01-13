document.addEventListener('DOMContentLoaded', function() {
    console.log('DomContentLoaded listener!');

    let pieces_picker = document.getElementById('pieces_picker');
    let height = 0;
    let pieces_selected = []
    let name = '';

    // keep the initial helper message
    let initial_pieces_picker_innerHTML_value = pieces_picker.innerHTML;

    document.getElementById('configuration-height-input').addEventListener('input', function(e) {
        console.log('input listener for #configuration-height-input!');

        let upper_limit = 10;
        let lower_limit = 1;

        if (e.target.value > 10) {
            e.target.value = 10;
        }

        if (e.target.value < 0) {
            e.target.value = 0;
        }

        let pickers_number = e.target.value;
        let innerHTML = initial_pieces_picker_innerHTML_value;
        let possible_pieces = document.getElementsByClassName('possible_piece');

        for (let i = 0; i < pickers_number; i++) {
            innerHTML += `
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <label class="input-group-text" for="piece-input">Piece</label>
                </div>
                <select class="custom-select" id="piece-input">
                    <option selected>Please pick a piece</option>
                `;

                for (let j = 0; j < possible_pieces.length; j++) {
                    innerHTML += '<option value="' + j + '">' + possible_pieces[j].textContent + '</option>';
                }

            innerHTML += `
                </select>
            </div>
            `
        }

        pieces_picker.innerHTML = innerHTML;
    });

    document.querySelector('#add_configuration_button').addEventListener('click', function(e) {
        console.log('add configuration button listener called!');

        let possible_pieces_values = []
        let possible_pieces = document.getElementsByClassName('possible_piece');
        for (let i = 0; i < possible_pieces.length; i++) {
            possible_pieces_values.push(possible_pieces[i].textContent.trim());
        }

        pieces_selected = [];
        let piece_pickers = document.getElementsByClassName('custom-select');

        height = 0;
        if (piece_pickers.length == 0) {
            alert('Height cannot be 0!');
            return;
        }
        height = piece_pickers.length;

        for (let i = 0; i < height; i++) {
            let option_picked = piece_pickers[i].value;

            if (isNaN(option_picked)) {
                pieces_selected = [];
                alert('Piece #' + i + ' was not chosen!');
                return;
            }

            let piece_value = piece_pickers[i].options[option_picked].text.trim();
            if (possible_pieces_values.includes(piece_value)) {
                pieces_selected.push(piece_value);
            }
        }

        console.log(pieces_selected);

        name = document.getElementById('configuration-name').value;
        if (name.length == 0) {
            alert("Invalid configuration name!");
            return;
        }

        document.querySelector('#add_configuration_form').submit();
    });

    document.querySelector('#add_configuration_form').addEventListener('submit', function (e) {
        console.log('addFormData() called!');

        e.preventDefault();

        new FormData(document.querySelector('#add_piece_form'));
    });

    document.querySelector('#add_configuration_form').addEventListener('formdata', (e) => {
        console.log('form data fired');

        e.preventDefault();

        let data = e.formData;

        data.append('height', height);
        data.append('selected_pieces', pieces_selected);
        data.append('name', name);

        for (var value of data.values()) {
            console.log(value);
        }
    });

}, false);