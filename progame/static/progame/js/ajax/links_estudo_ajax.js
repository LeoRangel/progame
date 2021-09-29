$('#adicionar-link-form').find('input').on('input', function() {
    resetInput($(this))
})

$('.card-header').delegate('a.links-estudo', 'click', function(e) {
    e.preventDefault()

    let botao = $(this)
    let modal = $('#links-estudo-modal')
    let get_url = botao.data('get-url')
    let post_url = botao.data('post-url')

    let form = modal.find('#adicionar-link-form')

    // atribui a url da requisição post para o formulário do modal
    form.attr('action', post_url)

    get_and_set_links(get_url, modal)
})


$('#adicionar-link-form').submit(function(e) {
    e.preventDefault()

    let form = $(this)
    let post_url = form.attr('action')

    let data = {};
    $(form.serializeArray()).each(function(i, field){
        data[field.name] = field.value;
    })

    make_ajax_post_request(post_url, data)
})


function make_ajax_post_request(url, data) {
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },

        url: url,
        type: "POST",
        dataType: 'JSON',
        data: data,

        success: function (data) {
            let lista = $('.links-estudo-list')

            let newElement = `
                <li id="${data.id}">
                    <a href="${data.url}" target="_blank">
                        <div class="imagem" style="background-image:url('/static/progame/img/open_in_new_tab.png')">
                        </div>
                        <div class="info">${getInfo(data)}</div>
                    </a>
                </li>
            `
            // lista.prepend($(newElement))
            $(newElement).prependTo(lista).hide().fadeIn()

            let prepended_element = $('#'+data.id)
            $('.no-link').hide()
            destacar_campo(prepended_element)
        },
        error: function(data) {
            // console.log('Erro:', data)
        },
        complete: function(data) {
            let form = $('#adicionar-link-form')
            removeErrors(form)
            form.find('button[type="submit"]').attr('disabled', false)
            let jsonData = data.responseJSON


            if (jsonData && 'errors' in jsonData) {
                let errors = jsonData.errors

                for (let field_name in errors) {
                    let input = $('#id_'+field_name)
                    let invalid_feedback = `<div class="invalid-feedback"><strong>${errors[field_name][0]}</strong></div>`

                    input.addClass('is-invalid');
                    $(invalid_feedback).insertAfter(input).show()
                }
            } else {
                form.trigger("reset");
            }
        }
    })
}


function get_and_set_links(url, modal) {
    let spinner = modal.find('.spinner')
    let no_link_message = modal.find('.no-link')
    let lista = modal.find('.links-estudo-list')

    $.ajax({
        url: url,
        type: "GET",
        dataType: 'JSON',
        cache: false,

        beforeSend: function() {
            let form = $('#adicionar-link-form')
            spinner.show()
            no_link_message.hide()
            lista.text('')
            removeErrors(form)
            form.trigger('reset')
        },
        success: function (data) {
            if (data.length > 0) {
                data.forEach(function(link) {
                    lista.append(`
                        <li id="${link.id}">
                            <a href="${link.url}" target="_blank">
                                <div class="imagem" style="background-image:url('/static/progame/img/open_in_new_tab.png')">
                                </div>
                                <div class="info">${getInfo(link)}</div>
                            </a>
                        </li>
                    `)
                })
            } else {
                no_link_message.show()
            }
        },
        error: function(data) {
            console.log('Erro: ', data)
        },
        complete: function() {
            spinner.hide()
        }
    })
}


function getInfo(data) {
    if (data.nome) {
        return `
            <p title="${data.nome}">${data.nome_trunc}</p>
            <span title="${data.url}">${data.url_trunc}</span>
        `
    } else if (data.url) {
        return `
            <p title="${data.url}">${data.url_trunc}</p>
        `
    }
}


function resetInput(input) {
    input.removeClass('is-invalid').siblings('.invalid-feedback').remove()
}

function removeErrors(form) {
    form.find('input').removeClass('is-invalid').siblings('.invalid-feedback').remove()
}
