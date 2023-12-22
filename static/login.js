var log_in = true;
function login() {

    var newls = document.querySelectorAll('.newl');
    newls.forEach(function (newl) {
        newl.style.visibility = 'hidden';
        newl.style.opacity = '0';
    });
    var newis = document.querySelectorAll('.newi');
    newis.forEach(function (newi) {
        newi.required = false;
        newi.style.border = 'none';
        newi.style.opacity = '0';
    });
    var stds = document.querySelectorAll('.normal');
    stds.forEach(function (std) {
        std.style.translate = '0 50px';
        std.style.visibility = 'visible';
        std.style.opacity = '1';
        std.required = true;
    });
    var reg = document.getElementById('reg')
    reg.style.border = '1.5px solid #dae9f7';
    reg.style.borderRadius = '5px';
    var log = document.getElementById('log')
    log.style.border = 'none';
    log.style.borderBottom = '1.5px solid #dae9f7';
    log.style.borderRadius = '0';

    log_in = true;
    return
}

function signup() {

    var newls = document.querySelectorAll('.newl');
    newls.forEach(function (newl) {
        newl.style.visibility = 'visible';
        newl.style.opacity = '1';
    });
    var newis = document.querySelectorAll('.newi');
    newis.forEach(function (newi) {
        newi.required = true;
        newi.style.border = '1.5px solid #dae9f7';
        newi.style.opacity = '1';
    });
    var stds = document.querySelectorAll('.normal');
    stds.forEach(function (std) {
        std.style.translate = '0 0';
        std.style.visibility = 'hidden';
        std.style.opacity = '0';
        std.required = false;
    });
    var reg = document.getElementById('reg')
    reg.style.border = 'none';
    reg.style.borderBottom = '1.5px solid #dae9f7';
    reg.style.borderRadius = '0';
    var log = document.getElementById('log')
    log.style.border = '1.5px solid #dae9f7';
    log.style.borderRadius = '5px';

    log_in = false;
    return
}