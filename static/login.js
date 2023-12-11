var log_in = true;
function login() {
    // document.getElementById('login').style.opacity = 1;
    // document.getElementById('signup').style.opacity = 0.5;
    // document.getElementById('login').style.fontSize = "x-large";
    // document.getElementById('signup').style.fontSize = "initial";

    const newls = document.querySelectorAll('.newl');
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
    const stds = document.querySelectorAll('.normal');
    stds.forEach(function (std) {
        std.style.translate = '0 50px';
    });
    // document.querySelector(':root').style.setProperty("--ph-c", "#191d2b");
    // document.getElementById('submit').style.translate = "0 -60px";
    // document.getElementById('part1').style.translate = "140px 0";
    log_in = true;
    return
}

function signup() {
    // document.getElementById('login').style.opacity = 0.5;
    // document.getElementById('signup').style.opacity = 1;
    // document.getElementById('login').style.fontSize = "initial";
    // document.getElementById('signup').style.fontSize = "x-large";

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
    const stds = document.querySelectorAll('.normal');
    stds.forEach(function (std) {
        std.style.translate = '0 0';
    });
    // document.querySelector(':root').style.setProperty("--ph-c", "#fff");
    // document.getElementById('submit').style.translate = "0 -30px";
    // document.getElementById('part1').style.translate = "0 0";

    log_in = false;
    return
}