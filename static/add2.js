// This script changes the options based on choice, bw product & log addition

function addp() {
    // For add product option

    // Hiding all log addition inputs
    var b2s = document.querySelectorAll('.b2');
    b2s.forEach(function (b2) {
        b2.style.visibility = 'hidden';
        b2.style.opacity = '0';
    });
    var b2is = document.querySelectorAll('.b2i');
    b2is.forEach(function (b2i) {
        b2i.required = false;
        b2i.style.border = 'none';
        b2i.style.opacity = '0';
    });

    // Making all product addition inputs visible
    var b1s = document.querySelectorAll('.b1');
    b1s.forEach(function (b1) {
        b1.style.visibility = 'visible';
        b1.style.opacity = '1';
    });
    var b1is = document.querySelectorAll('.b1i');
    b1is.forEach(function (b1i) {
        b1i.required = true;
        b1i.style.border = '1.5px solid #dae9f7';
        b1i.style.opacity = '1';
    });

    // Styling options to highlight choice
    var reg = document.getElementById('reg')
    reg.style.border = 'none';
    reg.style.borderBottom = '1.5px solid #dae9f7';
    reg.style.borderRadius = '0';
    var log = document.getElementById('log')
    log.style.border = '1.5px solid #dae9f7';
    log.style.borderRadius = '5px';

    // Positioning visible options properly
    document.getElementById('pid').style.position = 'relative';
    document.getElementById('pid').style.top = '0';
    var alls = document.querySelectorAll('.all');
    alls.forEach(function (all) {
        all.style.position = 'relative';
        all.style.bottom = '0';
    });
    // }
}

function add2sc() {
    // For adding log

    // Hiding product addition inputs
    var b1s = document.querySelectorAll('.b1');
    b1s.forEach(function (b1) {
        b1.style.visibility = 'hidden';
        b1.style.opacity = '0';
    });
    var b1is = document.querySelectorAll('.b1i');
    b1is.forEach(function (b1i) {
        b1i.required = false;
        b1i.style.border = 'none';
        b1i.style.opacity = '0';
    });

    // Making log addition inputs visible
    var b2s = document.querySelectorAll('.b2');
    b2s.forEach(function (b2) {
        b2.style.visibility = 'visible';
        b2.style.opacity = '1';
    });
    var b2is = document.querySelectorAll('.b2i');
    b2is.forEach(function (b2i) {
        b2i.required = true;
        b2i.style.border = '1.5px solid #dae9f7';
        b2i.style.opacity = '1';
        b2i.required = true;
    });

    // Styling options to highlight choice
    var log = document.getElementById('log')
    log.style.border = 'none';
    log.style.borderBottom = '1.5px solid #dae9f7';
    log.style.borderRadius = '0';
    var reg = document.getElementById('reg')
    reg.style.border = '1.5px solid #dae9f7';
    reg.style.borderRadius = '5px';

    // Positioning visible options properly
    document.getElementById('pid').style.position = 'relative';
    document.getElementById('pid').style.top = '65px';
    var alls = document.querySelectorAll('.all');
    alls.forEach(function (all) {
        all.style.position = 'relative';
        all.style.bottom = '100px';
    });
}