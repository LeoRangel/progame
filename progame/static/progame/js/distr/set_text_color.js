$(document).ready(function() {
    let header = $('#header');
    let rgb_string = header.css('background-color');

    const rgb = rgb_string.replace(/[^\d,]/g, '').split(',');

    // http://www.w3.org/TR/AERT#color-contrast
    const brightness = Math.round(((parseInt(rgb[0]) * 299) +
        (parseInt(rgb[1]) * 587) +
        (parseInt(rgb[2]) * 114)) / 1000);
    const textColor = (brightness > 125) ? 'black' : 'white';
    header.css('color', `${textColor} !important`);
});