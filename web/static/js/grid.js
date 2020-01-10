var selected_cells = []

function draw_cells() {
    console.log('start() called!');

    var grid = document.getElementById("grid_add_piece");

    var rows = document.getElementById('piece-height-input').value;
    var columns = document.getElementById('piece-width-input').value;

    grid.innerHTML = '';

    if (rows == 0 || columns == 0) {
        return;
    }

    for (i = 0; i < rows; i++) {

        var inner_columns = '';

        for (j = 0; j < columns; j++) {

            var current_cell = i * rows + j;

            inner_columns += `
            <div class="col">
                <div data="` + current_cell + `" class="cell" onclick="toggleCell(this, ` + current_cell + `)">
                       ` + current_cell + `
                </div>
            </div>
            `;
        }


        grid.innerHTML += '<div class="row">' + inner_columns + '</div>';
    }
}

function toggleCell(cell, current_cell) {

    console.log(cell.classList.contains("cell_selected"));

    cell.classList.toggle("cell_selected");

    if (cell.classList.contains("cell_selected")) {
        selected_cells.push(current_cell)
    }
    else {
        selected_cells.splice(selected_cells.indexOf(current_cell), 1);
    }

    console.log(selected_cells)
}

document.addEventListener('DOMContentLoaded', xx, false);

function xx () {
    console.log(document.URL);

    draw_cells();

    var piece_height = document.getElementById('piece-height-input');
    var piece_width = document.getElementById('piece-width-input');
    var piece_name = document.getElementById('piece-name');
    var piece_form = document.querySelector('#add_piece_form');

    piece_height.addEventListener('input', inputHandler);
    piece_width.addEventListener('input', inputHandler);
    piece_form.addEventListener('submit', newFormData);

    document.querySelector('#add_piece_button').addEventListener('click', addPiece);

    function inputHandler(e) {
        console.log(e.target.value);
        console.log(e.target.id);

        if (e.target.value > 11) {
            e.target.value = 11;
        }

        if (e.target.value < 1) {
            e.target.value = 1;
        }

         draw_cells();
    }

    function addPiece(e) {
        console.log('addPiece() called!');

        if (parseInt(piece_height.value) == 0) {
            alert("Invalid piece height!");
            return;
        }

        if (parseInt(piece_width.value) == 0) {
            alert("Invalid piece width!");
            return;
        }

        if (piece_name.value.length == 0) {
            alert("Invalid piece name!");
            return;
        }

        if (selected_cells.length == 0) {
            alert("You need to select at least one cell!");
            return;
        }

        document.querySelector('#add_piece_form').submit();
    }

    function newFormData() {
        console.log('addFormData() called!');

        e.preventDefault();

        new FormData(document.querySelector('#add_piece_form'));
    }

    document.querySelector('#add_piece_form').addEventListener('formdata', (e) => {
        console.log('form data fired');

        e.preventDefault();

        // Get the form data from the event object
        let data = e.formData;

        data.append('height', parseInt(piece_height.value));
        data.append('width', parseInt(piece_width.value));
        data.append('selected_cells', selected_cells);
        data.append('name', piece_name.value);

        for (var value of data.values()) {
            console.log(value);
        }
    });

}


