let $uploadCrop, rawImg;
function readFile(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();

        reader.onload = function (e) {
            $('#croppie-modal .modal-body').addClass('ready');
            $('#croppie-modal').modal('show')
            rawImg = e.target.result;
        };

        reader.readAsDataURL(input.files[0]);
    }
    else {
        alert("Sorry - you're browser doesn't support the FileReader API");
    }
}

$uploadCrop = $("#croppie-container").croppie({
    viewport: {
        width: 760,
        height: 300
    },
    // boundary: {
    //     width: 1110,
    //     height: 300
    // },
    enforceBoundary: false,
    enableExif: true
});

$("#croppie-modal").on("shown.bs.modal", function() {
    $uploadCrop
        .croppie("bind", {
            url: rawImg
        })
        .then(function() {
            console.log("jQuery bind complete");
        });
});

$('#croppie-input').on('change', function() { readFile(this) })
$('#upload-result').on('click', function (ev) {
    $uploadCrop.croppie('result', {
        type: 'base64',
        format: 'jpeg',
        size: 'viewport'
    }).then(function (resp) {
        //console.log(resp)
        //$("#result").attr("src", resp);

        $.ajax({
            url: '/turma/' + $('#croppie-input').data('pk') + '/atualizar_imagem/',
            data: {'image':resp},
            type: 'POST',

            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(data) {
                if (data.success === true) {
                    console.log('success', data)
                }
            },
            error: function(data) {
                console.log('error', data)
            },
            complete: function () {
                $("#croppie-modal").modal("hide");
            }
        })
    });
});