$('.card-header').delegate('a.quiz-toggle-bloqueio', 'click', function(e) {
    e.preventDefault()

    let botao = $(this)
    let url = botao.attr('href')
    let data = {
        modulo: botao.data('modulo'),
        nivel: botao.data('nivel')
    }
    let heading_id = 'heading' + botao.data('nivel')

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
        // async: false,

        success: function (data) {
            let bloqueado = data.bloqueado
            if (bloqueado) {
                Swal.fire({
                  icon: 'success',
                  title: 'Quiz bloqueado',
                  text: 'Agora os alunos não poderão respondê-lo até que você o desbloqueie',
                  // timer: 2500
                })
            } else if (!bloqueado) {
                Swal.fire({
                  icon: 'success',
                  title: 'Quiz desbloqueado',
                  text: 'Agora os alunos poderão respondê-lo',
                  // timer: 3000
                })
            }
            // let new_title = bloqueado ? 'Desbloquear quiz' : 'Bloquear quiz'
            $('#'+heading_id).load(' #' + heading_id + ' > *', function() {
                let botoes = $('#'+heading_id).find('.link-icon')
                botoes.each(function() {
                    let novo_botao = $(this)
                    novo_botao.attr('data-original-title', novo_botao.attr('title')).tooltip()
                })
            })
        },
        error: function(err) {
            console.log(err)
            Swal.fire({
              icon: 'error',
              title: 'Oops',
              text: 'Houve um erro. Por favor tente novamente',
              // timer: 3000
            })
        },
    })
})