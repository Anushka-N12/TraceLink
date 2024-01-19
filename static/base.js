//Styling navbar upon scrolling
function changeNav() {
  var h = document.getElementById('header')
  this.scrollY > 45 ? h.style.backgroundColor = 'rgba(1,1,1,1)' : h.style.backgroundColor = 'rgba(1,1,1,0)'

}
window.addEventListener("scroll", changeNav, false)