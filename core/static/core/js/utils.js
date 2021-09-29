// Prevenir mútiplas requisições
$("form.prevent-multi-submits").on("submit", function() {
    let form = $(this);
    let submit_button = form.find('button[type="submit"]');

    submit_button.attr("disabled", "true");
    submit_button.css('cursor', 'not-allowed');

    $(".spinner-submit").show();
});
