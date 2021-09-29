let modal = $('#participar_turma');
let codigo_input = $('#id_codigo');

$(document).ready(function() {
    modal.on('hidden.bs.modal', function() {
        resetCampo();
        codigo_input.val('')
    });

    modal.on('shown.bs.modal', function() {
        codigo_input.focus()
    });
});

$('#participar_turma_form').submit(function(e) {
    e.preventDefault();

    if (/([^\s])/.test(codigo_input.val())) {
        let form = $('#participar_turma_form');
        let formData = {};

        // pega dados do form e coloca em um object
        $(form.serializeArray()).each(function (i, field) {
            formData[field.name] = field.value;
        });

        codigo_input.on('input', function () {
            resetCampo()
        });

        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                }
            },

            url: form.attr('action'),
            type: "POST",
            dataType: "JSON",
            data: formData,

            success: function (data) {
                window.location.href = data.url
            },
            error: function (data) {
                let message = data.responseJSON.message;

                codigo_input.addClass('is-invalid');
                $('.invalid-feedback').text('').append('<strong>' + message + '</strong>').insertAfter(codigo_input).show()
            }
        });
    }
});

function resetCampo() {
    codigo_input.removeClass('is-invalid');
    $('.invalid-feedback').hide().text('')
}
