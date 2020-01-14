document.addEventListener('DOMContentLoaded', function() {
    console.log('DomContentLoaded listener!');

    let xhr = new XMLHttpRequest();
    let uploaded_file_details = document.getElementById('uploaded_file_details');
    let uploaded_file_current_innerHTML = '';
    let at_least_one_file_uploaded = false;
    let delete_default_message = true;

    document.getElementById('inputGroupFile01').addEventListener('change', function(e) {
        if (delete_default_message) {
            uploaded_file_details.innerHTML = '';
            delete_default_message = false;
        }

        let file_to_upload = this.files[0];

        if (file_to_upload != null) {
            let data = new FormData();
            data.append('upload_file', file_to_upload);

            let url = this.getAttribute('data');
            xhr.open("POST", url, true);
            xhr.send(data);

            if (at_least_one_file_uploaded == true) {
                uploaded_file_current_innerHTML += '<br>';
            }

            uploaded_file_current_innerHTML += '<div class="card text-center"><div class="card-body"><div class="row">';
            uploaded_file_current_innerHTML += '<div class="col alert alert-dark" role="alert" id="myalert">' + file_to_upload.name.trim() + '</div>';
        }
        else {
            console.log('File not picked!');
        }

        this.value = null; // set it on null in order to trigger it when the user tries to upload the same file consecutively
    });

    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if( xhr.status == 200) {
                console.log(xhr.responseText);

                let objectJSON = JSON.parse(xhr.responseText);

                if (objectJSON['success'] == true) {
                    uploaded_file_current_innerHTML += '<div class="col alert alert-success" role="alert" id="myalert">uploaded</div>';

                    if (objectJSON['supported'] == true) {
                        uploaded_file_current_innerHTML += '<div class="col alert alert-success" role="alert" id="myalert">supported</div>';
                    }
                    else {
                        uploaded_file_current_innerHTML += '<div class="col alert alert-danger" role="alert" id="myalert">supported</div>';
                    }
                }
                else {
                    uploaded_file_current_innerHTML += '<div class="col alert alert-danger" role="alert" id="myalert">uploaded</div>';
                }

                if (objectJSON['message'] != '') {
                    uploaded_file_current_innerHTML += '<div class="col-ms-2 alert alert-dark" role="alert" id="myalert">' + objectJSON['message'] + '</div>';
                }

            }
            else {
                console.log('There has been an error uploading the file!');
                uploaded_file_current_innerHTML += '<div class="col alert alert-danger" role="alert" id="myalert">There has been an error uploading the file! </div>';
            }

            uploaded_file_current_innerHTML += '</div></div></div>';

            uploaded_file_details.innerHTML += uploaded_file_current_innerHTML;
            uploaded_file_current_innerHTML = '';

            at_least_one_file_uploaded = true;
        }
    };

}, false);
