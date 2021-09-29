$(document).ready(function() {

    $('form').on('keyup keypress', function(e) {
        let keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });

    // $("input[type='radio']:checked").each(function() {
    //     $(this).parent().addClass('active')
    // });
    //
    // // selecionar o nível da questão
    // $('.nivel-radio-container').click(function() {
    //     let checked_id = $(this).find($("input[type='radio']")).attr('id');
    //
    //     $("input[type='radio']").each(function() {
    //         if ($(this).attr('id') === checked_id) {
    //             $(this).attr('checked', true);
    //             $(this).parent().addClass('active')
    //         } else {
    //             $(this).attr('checked', false);
    //             $(this).parent().removeClass('active')
    //         }
    //     })
    // });

    // adicionar alternativa pressionando enter
    $("input[name='alternativa']").on('keyup', function (e) {
        if (e.keyCode === 13) {
            e.preventDefault();
            adicionarAlternativa();
        }
    });

    // adicionar alternativa clicando no botão +
    $('#add_alternativa').click(function(e) {
        e.preventDefault();
        adicionarAlternativa();
    });

    // marcar alternativa como correta
    $('#alternativas').on('click', '.alternativa .nome', function() {
        let selecionada = $(this).closest('.alternativa');

        if (selecionada.hasClass('correta')) {
            selecionada.removeClass('correta').addClass('incorreta');
            selecionada.find('.nome').attr('data-original-title', 'Marcar como correta');
        } else {
            selecionada.removeClass('incorreta').addClass('correta');
            selecionada.find('.nome').attr('data-original-title', 'Marcar como incorreta');
        }
    });

    // excluir alternativa
    $('#alternativas').on('click', '.alternativa .excluir', function() {
        $('.tooltip').remove();

        $(this).closest('.alternativa').fadeOut(function() {
            $(this).remove();
            reorganizarLetras(); // reorganiza letras das alternativas
        });
    });
});


const alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u', 'v','w,','x','y','z'];

// função para adicionar uma alternativa
function adicionarAlternativa() {
    let input = $("input[name='alternativa']");

    if (/([^\s])/.test(input.val())) {  // verifica se input não está vazio
        let nova_alternativa = $('.alternativa').first().clone().css('display', 'table-row').appendTo($
        ('#alternativas'));
        let qtd_alternativas = $('#alternativas .alternativa').length - 1;  // pega a quantidade de alternativas
        nova_alternativa.find($('.nome')).tooltip().text(input.val());
        nova_alternativa.find($('.excluir')).tooltip();
        nova_alternativa.find('.identificador').text(alfabeto[qtd_alternativas-1] + ')')  // adiciona a letra na alternativa
        input.focus().val('');
    }
}

// função para adicionar várias alternativas
function adicionarAlternativas(alternativas) {
    if(alternativas) {
        alternativas.forEach(function(item) {
            let nova_alternativa = $('.alternativa').first().clone().css('display', 'table-row').appendTo($('#alternativas'));

            // pega a quantidade de alternativas para utilizar na adição da letra
            let qtd_alternativas = $('#alternativas .alternativa').length - 1;

            // se for correta, adicionar class correta
            item.fields.is_correta && nova_alternativa.removeClass('incorreta').addClass('correta');

            nova_alternativa.data('pk', item.pk);
            nova_alternativa.find($('.nome')).tooltip().text(item.fields.nome);
            nova_alternativa.find($('.excluir')).tooltip();
            nova_alternativa.find('.identificador').text(alfabeto[qtd_alternativas-1] + ')');  // adiciona a letra na alternativa
        });
    }
}


// reorganiza letras das alternativas
function reorganizarLetras() {
    contador = 0;
    $('.alternativa').each(function() {
        $(this).find($('.identificador')).text(alfabeto[contador-1] + ')');
        contador++;
    });
}