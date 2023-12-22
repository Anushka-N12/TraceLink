function add(inp1, inp1i, inp2, inp2i) {
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
    });
}
function addp() {
    add('.b2', '.b2i', '.b1', '.b1i')
}
function add2sc() {
    add('.b1', '.b1i', '.b2', '.b2i')
}