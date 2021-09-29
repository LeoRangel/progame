function destacar_campo(campo) {
    campo.css('transition-property', 'background');
    campo.css('transition-timing-function', 'ease-out');
    campo.css('transition-duration', '.2s');

    campo.css('background-color', '#e9f4ff');
    setTimeout(function() {
        campo.css('background-color', '#fff')
    }, 1500)
}