let clipboard = new ClipboardJS('.copiar');

function changeTooltipCopyText(element, message) {
    $(element).attr('data-original-title', message).tooltip('show');
    setTimeout(function() {
        $(element).attr('data-original-title', 'Copiar')
    }, 1000)
}

clipboard.on('success', function(e) {
    changeTooltipCopyText(e.trigger, 'Copiado!')
});