function add(inp1, inp1i, inp2, inp2i, b_1, b_2) {
    const b2s = document.querySelectorAll(inp1);
    b2s.forEach(function (b2) {
        b2.style.visibility = 'hidden';
        b2.style.opacity = '0';
    });
    var b2is = document.querySelectorAll(inp1i);
    b2is.forEach(function (b2i) {
        b2i.required = false;
        b2i.style.border = 'none';
        b2i.style.opacity = '0';
        b2.required = false;
    });
    var b1s = document.querySelectorAll(inp2);
    b1s.forEach(function (b1) {
        b1.style.visibility = 'visible';
        b1.style.opacity = '1';
    });
    var b1is = document.querySelectorAll(inp2i);
    b1is.forEach(function (b1i) {
        b1i.required = true;
        b1i.style.border = '1.5px solid #dae9f7';
        b1i.style.opacity = '1';
        b2.required = true;
    });
    var reg = document.getElementById(b_1)
    reg.style.border = 'none';
    reg.style.borderBottom = '1.5px solid #dae9f7';
    reg.style.borderRadius = '0';
    var log = document.getElementById(b_2)
    log.style.border = '1.5px solid #dae9f7';
    log.style.borderRadius = '5px';
    if (inp1 == '.b1') {
        document.getElementById('pid').style.position = 'relative';
        document.getElementById('pid').style.top = '120px';
        var alls = document.querySelectorAll('.all');
        alls.forEach(function (all) {
            all.style.position = 'relative';
            all.style.bottom = '100px';
        });
    }
    else {
        document.getElementById('pid').style.position = 'relative';
        document.getElementById('pid').style.top = '0';
        var alls = document.querySelectorAll('.all');
        alls.forEach(function (all) {
            all.style.position = 'relative';
            all.style.bottom = '0';
        });
    }
}
function addp() {
    add('.b2', '.b2i', '.b1', '.b1i', 'reg', 'log')
}
function add2sc() {
    add('.b1', '.b1i', '.b2', '.b2i', 'log', 'reg')
}