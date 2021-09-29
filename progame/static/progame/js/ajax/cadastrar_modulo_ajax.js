$('#form-cadastro-modulo').on('submit', function(e) {
    e.preventDefault();
    let alternativas_adicionadas = $('#alternativas .alternativa');
    let alternativas_corretas = $('#alternativas .alternativa.correta');

    if (alternativas_adicionadas.length > 2 && alternativas_corretas.length > 0) {
        let form = $(this);

        let formDataArray = form.serializeArray();
        let formDataObj = {};
        let alternativas = [];

        $(formDataArray).each(function(i, field){
            formDataObj[field.name] = field.value;
        });

        let counter = 0;
        form.find('.alternativa').each(function() {
            // ignorar primeira alternativa, pois ela não contém dados
            if (counter > 0) {
                let alternativa = $(this);

                alternativas.push(JSON.stringify({'nome': alternativa.find('.nome').text(), 'correta': alternativa.hasClass('correta')}))
            }
            counter++
        });

        let data = {
            'turma_uuid': form.data('turma'),
            'nome_modulo': formDataObj.nome_modulo,
            'descricao_modulo': formDataObj.descricao_modulo,
            'nivel_questao': formDataObj.nivel,
            'sentenca_questao': formDataObj.sentenca_questao,
            'descricao_questao': CKEDITOR.instances['id_descricao_questao'].getData(),
            'alternativas': alternativas
        };

        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },

            url: `/turma/${form.data('turma')}/modulo/adicionar/`,
            type: "POST",
            dataType: 'JSON',
            data: data,

            success: function (data) {
                //console.log(data);
                window.location.href = data.redirect_url
            },
            error: function(data) {
                console.log('Houve um erro:', data)
            }
        })
    } else if (alternativas_adicionadas.length <= 2) {
        $('.invalid-alternativa').show().text('Adicione pelo menos duas alternativas')
    } else if (alternativas_corretas.length <= 0) {
        $('.invalid-alternativa').show().text('Marque pelo menos uma alternativa como correta')
    }
});

$('#pular-questao').click(function(e) {
    e.preventDefault();
    let url = $(this).attr('href');
    let formDataArray = $('#form-cadastro-modulo').serializeArray();
    let formDataObj = {};

    $(formDataArray).each(function(i, field){
        formDataObj[field.name] = field.value;
    });

    let data = {
        nome_modulo: formDataObj.nome_modulo,
        descricao_modulo: formDataObj.descricao_modulo,
    }

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
            // console.log('Sucesso: ', data);
            window.location.href = data.redirect_url
        },
        error: function(data) {
            if (data.responseJSON.message === 'form_invalid') {
                $('.validation-wizard .actions').find($('a[href="#previous"]')).click()
                Swal.fire({
                  icon: 'error',
                  title: 'Dados inválidos',
                  text: 'Preencha os campos obrigatórios e tente novamente',
                })
            }
        }
    })
});
