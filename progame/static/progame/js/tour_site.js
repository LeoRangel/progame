

// Para resolver problema no bootstrap tour de não ficar com
// height do backdrop (tela escura) 100%
$(document).ready(function() {
    $bodyWidth = $(window).width();
    $bodyHeight = $(window).height();
    $(".tour-backdrop").css("width", $bodyWidth);
    $(".tour-backdrop").css("height", $bodyHeight);
});

$(window).resize(function() {
    $bodyWidth = $(window).width();
    $bodyHeight = $(window).height();
    $(".tour-backdrop").css("width", $bodyWidth);
    $(".tour-backdrop").css("height", $bodyHeight);
});




// Função que cria o Tour pelo site (recebe os passos de cada página)
function site_tour(passos, nome){

    var tour = new Tour({
        framework: 'bootstrap4',   // or "bootstrap4" depending on your version of bootstrap
        name: nome,
        // storage: false,
        keyboard: true,
        // debug: true,
        localization: {
            buttonTexts: {
                prevButton:  "<i class='fas fa-arrow-left'></i>",
                nextButton:  "<i class='fas fa-arrow-right'></i>",
                pauseButton:  "Pausa",
                resumeButton:  "Continuar",
                endTourButton:  "Finalizar dicas",
            },
        },
        steps: passos['steps'],
        // container: "body",
        autoscroll: true,
        backdrop: true,
        backdropContainer: 'body',
    });

    // tour.restart();
    // tour.init();
    tour.start();
    
}